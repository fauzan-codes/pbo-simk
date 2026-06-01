from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from farmasi.models import Resep, DetailResep
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def konfirmasi_resep_index(request):
    daftar_resep = Resep.objects.select_related('rekam_medis', 'apoteker').filter(status='diproses').all()
    
    context = {
        'daftar_resep': daftar_resep,
        'page_title': 'Konfirmasi Resep Doker',
    }
    return render(request, 'pages/farmasi/konfirmasi_resep/index.html', context)

@login_required
def konfirmasi_resep_detail(request, id):
    resep = get_object_or_404(Resep, pk=id)
    detail_resep = DetailResep.objects.select_related('obat').filter(resep=resep).all()
    
    context = {
        'resep': resep,
        'detail_resep': detail_resep,
        'page_title': 'Detail Resep Doker',
    }
    return render(request, 'pages/farmasi/konfirmasi_resep/detail.html', context)

@login_required
def konfirmasi_resep_confirm(request, id):
    resep = get_object_or_404(Resep, pk=id)
    
    try:
        resep.status = 'selesai'
        resep.save()
        messages.success(request, 'Resep berhasil dikonfirmasi.')
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')
    
    return redirect('konfirmasi_resep_index')
