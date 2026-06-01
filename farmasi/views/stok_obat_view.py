from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from farmasi.models import Obat
from farmasi.models import KategoriObat
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def stok_obat_index(request):
    daftar_obat = Obat.objects.select_related('kategori').all()
    
    context = {
        'daftar_obat': daftar_obat,
        'page_title': 'Stok Obat',
        'breadcrumbs': [
            {'name': 'Stok Obat', 'url': reverse('stok_obat_index')},
        ],
    }
    return render(request, 'pages/farmasi/stok_obat/index.html', context)

@login_required
def stok_obat_create(request):
    if request.method == "POST":
        try:
            nama_obat = request.POST.get('nama_obat')
            kode_obat = request.POST.get('kode_obat')
            kategori_id = request.POST.get('kategori')
            stok = int(request.POST.get('stok', 0))
            harga_jual = request.POST.get('harga')
            satuan = request.POST.get('satuan')
            
            
            obat = Obat.objects.create(
                nama_obat = nama_obat,
                kategori_id = kategori_id,
                kode_obat = kode_obat,
                stok = stok,
                harga_jual = harga_jual,
                satuan = satuan,
            )
            
            messages.success(request, f'Data obat {nama_obat} berhasil ditambahkan.')
            return redirect('stok_obat_index')
            
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
    
    kategori = KategoriObat.objects.all()
    
    context = {
        'kategori_options': [(d.id, d.nama_kategori) for d in kategori],
        'page_title': 'Tambah Stok Obat',
        'breadcrumbs': [
            {'name': 'Stok Obat', 'url': reverse('stok_obat_index')},
            {'name': 'Tambah Stok', 'url': None},
        ],
    }
    
    return render(request, 'pages/farmasi/stok_obat/create.html', context)

@login_required
def stok_obat_edit(request, id):
    obat = get_object_or_404(Obat, pk=id)
    
    if request.method == "POST":
        try:
            nama_obat = request.POST.get('nama_obat')
            kode_obat = request.POST.get('kode_obat')
            kategori = request.POST.get('kategori')
            stok = int(request.POST.get('stok', 0))
            harga_jual = request.POST.get('harga')
            satuan = request.POST.get('satuan')
            
            obat.nama_obat = nama_obat
            obat.kode_obat = kode_obat
            obat.kategori_id = kategori
            obat.stok = stok
            obat.harga_jual = harga_jual
            obat.satuan = satuan
            
            obat.save()
            messages.success(request, f'Data obat {nama_obat} berhasil diperbarui.')
            return redirect('stok_obat_index')
            
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
    
    kategori = KategoriObat.objects.all()
    
    context = {
        'obat': obat,
        'kategori_options': [(d.id, d.nama_kategori) for d in kategori],
        'page_title': 'Edit Stok Obat',
        'breadcrumbs': [
            {'name': 'Stok Obat', 'url': reverse('stok_obat_index')},
            {'name': 'Edit Stok', 'url': None},
        ],
    }
    
    return render(request, 'pages/farmasi/stok_obat/edit.html', context)

@login_required
def stok_obat_delete(request, id):
    Obat.objects.get(id=id).delete()
    messages.success(request, 'Data obat berhasil dihapus.')
    return redirect('stok_obat_index')