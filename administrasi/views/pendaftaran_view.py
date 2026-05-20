import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from pelayanan.models import Kunjungan
from accounts.models import Pasien
from master_data.models import JadwalPraktik
from administrasi.models import Tiket
from django.urls import reverse

def get_jadwal():
    semua_jadwal = JadwalPraktik.objects.select_related('dokter__user', 'poli').all()
    jadwal_dict = {}
    for j in semua_jadwal:
        hari_key = j.hari.lower() 
        if hari_key not in jadwal_dict:
            jadwal_dict[hari_key] = []
            
        label = f"{j.dokter.user.full_name} - Poli {j.poli.nama_poli} ({j.jam_mulai.strftime('%H:%M')} - {j.jam_selesai.strftime('%H:%M')})"
        
        jadwal_dict[hari_key].append({
            'value': j.id,
            'label': label
        })

    return json.dumps(jadwal_dict)

@login_required
def daftar_online_index(request):
    if request.method == "POST":
        pasien_id = request.user.pasien_profile.id
        tanggal_kunjungan = request.POST.get('tanggal_kunjungan')
        jadwal_id = request.POST.get('jadwal_id')

        jadwal = JadwalPraktik.objects.get(id=jadwal_id)
        nomor_baru = Kunjungan.generateNomorAntrean(jadwal=jadwal, tanggal_kunjungan=tanggal_kunjungan)

        kunjungan = Kunjungan.objects.create(
            pasien_id = pasien_id,
            tanggal_kunjungan = tanggal_kunjungan,
            jadwal_id = jadwal_id,
            nomor_antrean=nomor_baru,
            status = "dipesan"
        )

        Tiket.objects.create(
            pasien_id = pasien_id,
            kunjungan_id = kunjungan.id
        )

        messages.success(request, f'Berhasil mendaftarkan pasien')

        return redirect('dashboard')

    context = {
        'breadcrumbs': [
            {'name': 'Dashboard', 'url': reverse('dashboard')},
            {'name': 'Daftar Online', 'url': reverse('daftar_online_index')},
        ],
        'page_title': 'Daftar Online',
        'jadwal_data_json': get_jadwal(),
    }

    return render(request, 'pages/administrasi/daftar_online/index.html', context)

@login_required
def cetak_tiket(request, no_tiket):
    tiket = get_object_or_404(Tiket, no_tiket=no_tiket)
    
    context = {
        'tiket': tiket,
    }   
    
    return render(request, 'pages/administrasi/daftar_online/tiket.html', context)