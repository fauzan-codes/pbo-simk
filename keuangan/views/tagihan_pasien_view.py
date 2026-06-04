from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pelayanan.models import Kunjungan
from ..models import Tagihan, MetodePembayaran
from django.utils import timezone
from django.urls import reverse

@login_required
def keuangan_tagihan_index(request):
    data_kunjungan = Kunjungan.objects.filter(status='selesai')
    context = {
        'data_kunjungan': data_kunjungan,
        'breadcrumbs': [
            {'name': 'Tagihan Pasien', 'url': reverse('keuangan_tagihan_index')},
        ],
        'page_title': 'Tagihan Pasien'
    }
    return render(request, 'pages/keuangan/tagihan_pasien/index.html', context)

@login_required
def buat_tagihan_index(request, id):
    data_kunjungan = Kunjungan.objects.get(id=id)
    metode_bayar = MetodePembayaran.objects.all()

    daftar_tindakan = []
    daftar_obat = []
    subtotal_tindakan = 0
    subtotal_obat = 0

    if hasattr(data_kunjungan, 'rekammedis'):
        rekam_medis = data_kunjungan.rekammedis
        
        daftar_tindakan = rekam_medis.tindakanrekammedis_set.all()
        subtotal_tindakan = sum(t.tindakan_medis.tarif for t in daftar_tindakan)
        
        for resep in rekam_medis.resep_set.all():
            detail_resep = resep.detailresep_set.all()
            daftar_obat.extend(detail_resep)
            subtotal_obat += sum(d.subtotal_harga for d in detail_resep)

    grand_total = subtotal_tindakan + subtotal_obat

    if request.method == 'POST':
        metode_id = request.POST.get('metode_pembayaran')
        rekam_medis = data_kunjungan.rekammedis
        total_tindakan = sum(t.tindakan_medis.tarif for t in rekam_medis.tindakanrekammedis_set.all())
        total_obat = 0
        for resep in rekam_medis.resep_set.all():
            total_obat += sum(d.subtotal_harga for d in resep.detailresep_set.all())

        if not request.user.role == 'staff':
            messages.error(request, f'Akun ini bukan akun staff.')
            return redirect('keuangan_tagihan_index')

        Tagihan.objects.create(
            total_biaya_tindakan=total_tindakan,
            total_biaya_obat=total_obat,
            grand_total=total_tindakan + total_obat,
            status_pembayaran='lunas',
            waktu_pembayaran=timezone.now(),
            kasir_id=request.user.staff_profile.id,
            kunjungan_id=id,
            metode_bayar_id=metode_id,
        )

        data_kunjungan.status = 'lunas'
        data_kunjungan.save()

        return redirect('keuangan_tagihan_index')
    
    context = {
        'data_kunjungan': data_kunjungan,
        'metode_bayar': metode_bayar,
        'metode_options':  [(m.id, m.nama_metode) for m in metode_bayar],
        'daftar_tindakan': daftar_tindakan,
        'daftar_obat': daftar_obat,
        'subtotal_tindakan': subtotal_tindakan,
        'subtotal_obat': subtotal_obat,
        'grand_total': grand_total,
        'breadcrumbs': [
            {'name': 'Tagihan Pasien', 'url': reverse('keuangan_tagihan_index')},
            {'name': 'Buat Tagihan', 'url': None},
        ],
        'page_title': 'Buat Tagihan'
    }
    return render(request, 'pages/keuangan/tagihan_pasien/details.html', context)
