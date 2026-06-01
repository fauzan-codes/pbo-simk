from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import MetodePembayaran
from django.urls import reverse

@login_required
def metode_pembayaran_index(request):
    metode_list = MetodePembayaran.objects.all()
    context = {
        'metode_list': metode_list,
        'breadcrumbs': [
            {'name': 'Metode Pembayaran', 'url': reverse('metode_pembayaran_index')},
        ],
        'page_title': 'Metode Pembayaran'
    }
    return render(request, 'pages/keuangan/metode_pembayaran/index.html', context)

@login_required
def metode_pembayaran_create(request):
    if request.method == "POST":
        try: 
            nama_metode = request.POST.get('nama_metode')

            MetodePembayaran.objects.create(
                nama_metode = nama_metode
            )
            messages.success(request, f"Metode {nama_metode} berhasil ditambahkan.")
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return redirect('metode_pembayaran_index')

@login_required
def metode_pembayaran_edit(request, id):
    try:
        metode = MetodePembayaran.objects.get(id=id)
    except metode.DoesNotExist:
        messages.error(request, "Metode tidak ditemukan.")
        return redirect('metode_pembayaran_index')

    if request.method == "POST":
        try:
            nama_metode = request.POST.get('nama_metode')
            metode.nama_metode = nama_metode
            metode.save()
            messages.success(request, f'Metode {nama_metode} berhasil diupdate')
            return redirect('metode_pembayaran_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    context = {
        'metode': metode,
        'breadcrumbs': [
            {'name': 'Metode Pembayaran', 'url': reverse('metode_pembayaran_index')},
            {'name': 'Edit Metode Pembayaran', 'url': None},
        ],
        'page_title': 'Edit Metode Pembayaran'
    }
    return render(request, 'pages/keuangan/metode_pembayaran/edit.html', context)

@login_required
def metode_pembayaran_delete(request, id):
    try:
        metode = MetodePembayaran.objects.get(id=id)
        metode.delete()
        messages.success(request, "Metode pembayaran berhasil dihapus")
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return redirect('metode_pembayaran_index')