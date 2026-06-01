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