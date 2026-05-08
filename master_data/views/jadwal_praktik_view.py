from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import JadwalPraktik, Poli
from accounts.models import Dokter
from django.urls import reverse
from ..forms import JadwalForm

@login_required
def jadwal_praktik_index(request):
    hari_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
    
    jadwal_dict = {}
    
    for hari in hari_list:
        jadwal_dict[hari] = JadwalPraktik.objects.filter(hari__iexact=hari).order_by('jam_mulai')

    context = {
        'jadwal_dict': jadwal_dict, 
        'breadcrumbs': [
            {'name': 'Jadwal Praktik', 'url': reverse('jadwal_praktik_index')},
        ],
        'page_title': 'Jadwal Praktik'
    }
    
    return render(request, 'pages/master/jadwal_praktik/index.html', context)

@login_required
def jadwal_praktik_create(request):
    form = JadwalForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            JadwalPraktik.objects.create(
                dokter_id = request.POST.get('dokter_id'),
                poli_id = request.POST.get('poli_id'),
                hari = request.POST.get('hari'),
                jam_mulai = request.POST.get('jam_mulai'),
                jam_selesai = request.POST.get('jam_selesai')
            )

            messages.success(request, f'Data jadwal praktik berhasil ditambahkan.')
            return redirect('jadwal_praktik_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    dokters = Dokter.objects.all()
    polis = Poli.objects.all()

    context = {
        'form': form,
        'dokter_options': [(d.id, d.user.full_name) for d in dokters],
        'poli_options': [(p.id, p.nama_poli) for p in polis],
        'hari_options': [(hari, hari) for hari in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']],
        'breadcrumbs': [
                {'name': 'Jadwal Pratik', 'url': reverse('jadwal_praktik_index')},
                {'name': 'Buat Jadwal Praktik', 'url': None},
        ],
        'page_title': 'Buat Jadwal Praktik'
    }
    return render(request, 'pages/master/jadwal_praktik/create.html', context)

@login_required
def jadwal_praktik_edit(request, id):
    try:
        jadwal = JadwalPraktik.objects.get(id=id)
    except jadwal.DoesNotExist:
        messages.error(request, "Jadwal tidak ditemukan.")
        return redirect('jadwal_praktik_index')
    
    
    if request.method == "POST":
        try:
            jadwal.dokter_id = request.POST.get('dokter_id')
            jadwal.poli_id = request.POST.get('poli_id')
            jadwal.hari = request.POST.get('hari')
            jadwal.jam_mulai = request.POST.get('jam_mulai')
            jadwal.jam_selesai = request.POST.get('jam_selesai')
            jadwal.save()

            messages.success(request, f'Data jadwal praktik berhasil diupdate.')
            return redirect('jadwal_praktik_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    dokters = Dokter.objects.all()
    polis = Poli.objects.all()

    context = {
        'jadwal': jadwal,
        'dokter_options': [(d.id, d.user.full_name) for d in dokters],
        'poli_options': [(p.id, p.nama_poli) for p in polis],
        'hari_options': [(hari, hari) for hari in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']],
        'breadcrumbs': [
            {'name': 'Jadwal Pratik', 'url': reverse('jadwal_praktik_index')},
            {'name': 'Edit Jadwal Praktik', 'url': None},
        ],
        'page_title': 'Edit Jadwal Praktik'
    }
    return render(request, 'pages/master/jadwal_praktik/edit.html', context)

@login_required
def jadwal_praktik_delete(request, id):
    try:
        jadwal = JadwalPraktik.objects.get(id=id)
        jadwal.delete()
        messages.success(request, 'Data jadwal praktik berhasil dihapus.')
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return redirect('jadwal_praktik_index')