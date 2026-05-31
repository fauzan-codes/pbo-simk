import json
from django.shortcuts import render, redirect
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
def check_in_index(request):
    context = {
        'breadcrumbs': [
            {'name': 'Check In', 'url': reverse('check_in_index')},
        ],
        'page_title': 'Check In',
    }

    return render(request, 'pages/administrasi/check_in/index.html', context)

@login_required
def check_in_online(request):
    context = {
        'breadcrumbs': [
            {'name': 'Check In', 'url': reverse('check_in_index')},
            {'name': 'Online', 'url': reverse('check_in_online')},
        ],
        'page_title': 'Pendaftaran Online',
        'show_modal': False
    }

    if request.method == "POST":
        no_tiket = request.POST.get('no_tiket')
        
        try:
            tiket = Tiket.objects.select_related('kunjungan').get(no_tiket=no_tiket)
            kunjungan = tiket.kunjungan
            
            if kunjungan.status == 'dipesan':
                
                Kunjungan.changeStatus(kunjungan.id, 'menunggu')
                
                kunjungan.status = 'menunggu'
                
                messages.success(request, "Check-in berhasil! Status kunjungan telah diubah.")
                context['show_modal'] = True
                context['kunjungan'] = kunjungan 
                context['no_tiket'] = no_tiket
                
            elif kunjungan.status == 'menunggu':
                messages.warning(request, f"Pasien dengan tiket {no_tiket} sudah melakukan check-in sebelumnya.")
                
            else:
                messages.error(request, f"Check-in ditolak. Status pasien saat ini adalah: '{kunjungan.status}'.")

        except Tiket.DoesNotExist:
            messages.error(request, f"Nomor tiket '{no_tiket}' tidak ditemukan di sistem.")

    return render(request, 'pages/administrasi/check_in/online.html', context)

@login_required
def check_in_offline(request):
    if request.method == "POST":
        pasien_id = request.POST.get('pasien_id')
        tanggal_kunjungan = request.POST.get('tanggal_kunjungan')
        jadwal_id = request.POST.get('jadwal_id')

        jadwal = JadwalPraktik.objects.get(id=jadwal_id)
        nomor_baru = Kunjungan.generateNomorAntrean(jadwal=jadwal, tanggal_kunjungan=tanggal_kunjungan)

        kunjungan = Kunjungan.objects.create(
            pasien_id = pasien_id,
            tanggal_kunjungan = tanggal_kunjungan,
            jadwal_id = jadwal_id,
            nomor_antrean=nomor_baru,
            status="menunggu"
        )

        messages.success(request, f'Berhasil mendaftarkan pasien dengan nomor antrean {kunjungan.kode_antrean}')

        request.session['tiket_baru'] = {
            'kode_antrean': kunjungan.kode_antrean,
            'nama_pasien': kunjungan.pasien.user.full_name, 
            'poli': jadwal.poli.nama_poli,
            'tanggal': tanggal_kunjungan
        }

        return redirect('check_in_offline')

    semua_pasien = Pasien.objects.select_related('user').all()
    
    pasien_options = []
    for pasien in semua_pasien:
        nama_lengkap = pasien.user.full_name if pasien.user else "Tanpa Nama"
        
        label = f"{pasien.nomor_rekam_medis} - {nama_lengkap}"
        
        pasien_options.append((pasien.id, label))

    context = {
        'breadcrumbs': [
            {'name': 'Check In', 'url': reverse('check_in_index')},
            {'name': 'Offline', 'url': reverse('check_in_offline')},
        ],
        'page_title': 'Pendaftaran Offline',
        'pasien_options': pasien_options,
        'jadwal_data_json': get_jadwal(),
    }

    if 'tiket_baru' in request.session:
        context['tiket_baru'] = request.session.pop('tiket_baru')

    return render(request, 'pages/administrasi/check_in/offline.html', context)