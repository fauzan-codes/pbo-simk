from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from administrasi.models import Poli
from django.urls import reverse

@login_required
def poli_index(request):
    poli_list = Poli.objects.all()
    context = {
        'poli_list': poli_list,
        'breadcrumbs': [
            {'name': 'Manajemen Poli', 'url': reverse('poli_index')},
        ],
        'page_title': 'Manajemen Poli'
    }
    return render(request, 'pages/administrasi/poli/index.html', context)

@login_required
def poli_create(request):
    if request.method == "POST":
        try:
            nama_poli = request.POST.get('nama_poli')
            kode_poli = request.POST.get('kode_poli')

            Poli.objects.create(
                nama_poli = nama_poli,
                kode_poli = kode_poli
            )

            messages.success(request, f'Data {nama_poli} berhasil ditambahkan.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return redirect('poli_index')

@login_required
def poli_edit(request, id):
    try:
        poli = Poli.objects.get(id=id)
    except poli.DoesNotExist:
        messages.error(request, "Poli tidak ditemukan.")
        return redirect('poli_index')
    
    if request.method == "POST":
        try:
            nama_poli = request.POST.get('nama_poli')
            poli.nama_poli =  nama_poli
            poli.save()

            messages.success(request, f'Data {nama_poli} berhasil diupdate.')
            return redirect('poli_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    context = {
        'poli': poli,
        'breadcrumbs': [
            {'name': 'Manajemen Poli', 'url': reverse('poli_index')},
            {'name': 'Edit Poli', 'url': None},
        ],
        'page_title': 'Edit Poli'
    }
    return render(request, 'pages/administrasi/poli/edit.html', context)

@login_required
def poli_delete(request, id):
    try:
        poli = Poli.objects.get(id=id)
        poli.delete()
        messages.success(request, 'Data poli berhasil dihapus.')
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return redirect('poli_index')