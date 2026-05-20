from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import KategoriObat
from django.urls import reverse

@login_required
def kategori_obat_index(request):
    kategori_list = KategoriObat.objects.all()
    context = {
        'kategori_list': kategori_list, 
        'breadcrumbs': [
            {'name': 'Kategori Obat', 'url': reverse('kategori_obat_index')},
        ],
        'page_title': 'Kategori Obat'
    }
    return render(request, 'pages/farmasi/kategori/index.html', context)

@login_required
def kategori_obat_create(request):
    if request.method == "POST":
        try:
            nama_kategori = request.POST.get('nama_kategori')

            KategoriObat.objects.create(
                nama_kategori = nama_kategori,
            )

            messages.success(request, f'Data {nama_kategori} berhasil ditambahkan.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return redirect('kategori_obat_index')

@login_required
def kategori_obat_edit(request, id):
    try:
        kategori = KategoriObat.objects.get(id=id)
    except kategori.DoesNotExist:
        messages.error(request, "Kategori tidak ditemukan.")
        return redirect('kategori_obat_index')
    
    if request.method == "POST":
        try:
            nama_kategori = request.POST.get('nama_kategori')
            kategori.nama_kategori =  nama_kategori
            kategori.save()

            messages.success(request, f'Data {nama_kategori} berhasil diupdate.')
            return redirect('kategori_obat_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    context = {
        'kategori': kategori,
        'breadcrumbs': [
            {'name': 'Kategori Obat', 'url': reverse('kategori_obat_index')},
            {'name': 'Edit Kategori Obat', 'url': None},
        ],
        'page_title': 'Edit Kategori Obat'
    }
    return render(request, 'pages/farmasi/kategori/edit.html', context)

@login_required
def kategori_obat_delete(request, id):
    try:
        kategori = KategoriObat.objects.get(id=id)
        kategori.delete()
        messages.success(request, 'Data kategori obat berhasil dihapus.')
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return redirect('kategori_obat_index')