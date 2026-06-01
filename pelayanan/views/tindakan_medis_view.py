from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from pelayanan.models import TindakanMedis
from django.urls import reverse

@login_required
def tindakan_medis_index(request):
    tindakan_list = TindakanMedis.objects.all()
    context = {
        'tindakan_list': tindakan_list,
        'breadcrumbs': [
            {'name': 'Tindakan Medis', 'url': reverse('tindakan_medis_index')},
        ],
        'page_title': 'Tindakan Medis'
    }
    return render(request, 'pages/pelayanan/tindakan_medis/index.html', context)

@login_required
def tindakan_medis_create(request):
    if request.method == "POST":
        try:
            nama_tindakan = request.POST.get('nama_tindakan')
            tarif = request.POST.get('tarif')

            TindakanMedis.objects.create(
                nama_tindakan = nama_tindakan,
                tarif = tarif
            )

            messages.success(request, f'Data {nama_tindakan} berhasil ditambahkan.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return redirect('tindakan_medis_index')

@login_required
def tindakan_medis_edit(request, id):
    try:
        tindakan = TindakanMedis.objects.get(id=id)
    except tindakan.DoesNotExist:
        messages.error(request, "Tindakan medis tidak ditemukan.")
        return redirect('tindakan_medis_index')
    
    if request.method == "POST":
        try:
            nama_tindakan = request.POST.get('nama_tindakan')
            tindakan.nama_tindakan =  nama_tindakan
            tindakan.tarif = request.POST.get('tarif')
            tindakan.save()

            messages.success(request, f'Data {nama_tindakan} berhasil diupdate.')
            return redirect('tindakan_medis_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    context = {
        'tindakan': tindakan,
        'breadcrumbs': [
            {'name': 'Tindakan Medis', 'url': reverse('tindakan_medis_index')},
            {'name': 'Edit Tindakan Medis', 'url': None},
        ],
        'page_title': 'Edit Tindakan Medis'
    }
    return render(request, 'pages/pelayanan/tindakan_medis/edit.html', context)

@login_required
def tindakan_medis_delete(request, id):
    try:
        tindakan = TindakanMedis.objects.get(id=id)
        tindakan.delete()
        messages.success(request, 'Data tindakan medis berhasil dihapus.')
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return redirect('tindakan_medis_index')