from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from keuangan.models import Tagihan
from django.urls import reverse

@login_required
def keuangan_riwayat_index(request):
    data_tagihan = Tagihan.objects.all()
    context = {
        'data_tagihan': data_tagihan,
        'breadcrumbs': [
            {'name': 'Riwayat Pembayaran', 'url': reverse('keuangan_riwayat_index')},
        ],
        'page_title': 'Riwayat Pembayaran'
    }
    return render(request, 'pages/keuangan/riwayat_pembayaran/index.html', context)

def keuangan_riwayat_details(request, id):
    daftar_tindakan = []
    daftar_obat = []

    data_tagihan = Tagihan.objects.get(id=id)
    if hasattr(data_tagihan.kunjungan, 'rekammedis'):
        rekam_medis = data_tagihan.kunjungan.rekammedis
        
        daftar_tindakan = rekam_medis.tindakanrekammedis_set.all()
        
        for resep in rekam_medis.resep_set.all():
            detail_resep = resep.detailresep_set.all()
            daftar_obat.extend(detail_resep)

    context = {
        'data_tagihan': data_tagihan,
        'daftar_tindakan': daftar_tindakan,
        'daftar_obat': daftar_obat,
        'breadcrumbs': [
            {'name': 'Riwayat Pembayaran', 'url': reverse('keuangan_riwayat_index')},
            {'name': 'Detail Tagihan', 'url': None},
        ],
        'page_title': 'Detail Tagihan'
    }
    return render(request, 'pages/keuangan/riwayat_pembayaran/details.html', context)