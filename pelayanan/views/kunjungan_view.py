from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Kunjungan
from django.urls import reverse

@login_required
def kunjungan_index(request):
    kunjungan_list = Kunjungan.objects.all()
    kunjungan = Kunjungan.objects.get(id=id)

    user = kunjungan.pasien

    context = {
        'kunjugan_list': kunjungan_list,
        'breadcrumbs': [
            {'name': 'Kategori Obat', 'url': reverse('kategori_obat_index')},
        ],
        'page_title': 'Kategori Obat'
    }
    return render(request, 'pages/farmasi/kategori/index.html', context)