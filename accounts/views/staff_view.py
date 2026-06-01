from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import User, Staff
from django.urls import reverse

from ..services.staff_service import StaffService
from ..forms import StaffForm

@login_required
def staff_index(request):
    users = User.objects.filter(role='staff').order_by('-id')
    context = {
        'users': users,
        'breadcrumbs': [
            {'name': 'Manajemen Staff', 'url': reverse('staff_index')},
        ],
        'page_title': 'Manajemen Staff'
    }
    return render(request, 'pages/accounts/staff/index.html', context)

@login_required
def staff_create(request):
    form = StaffForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            data = form.cleaned_data
            user_data = {k: data[k] for k in ['username', 'full_name', 'email', 'password']}
            pasien_data = {k: data[k] for k in ['jabatan', 'shift_kerja', 'alamat', 'no_hp']}
            StaffService.create_staff(user_data, pasien_data)
            messages.success(request, f"Staff {data['full_name']} berhasil didaftarkan.")
            return redirect('staff_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
    context = {
        'form': form,
        'breadcrumbs': [
            {'name': 'Manajemen Staff', 'url': reverse('staff_index')},
            {'name': 'Registrasi Staff', 'url': None},
        ],
        'page_title': 'Tambah Staff Baru',
        'jabatan_options' : [
            ('Administrasi', 'Administrasi'),
            ('Kasir', 'Kasir'),
            ('Apoteker', 'Apoteker'),
        ]
    }
    return render(request, 'pages/accounts/staff/create.html', context)


@login_required
def staff_edit(request, id):
    try:
        staff = Staff.objects.get(id=id)
    except Staff.DoesNotExist:
        messages.error(request, "Staff tidak ditemukan.")
        return redirect('staff_index')

    initial_data = {
        'username': staff.user.username,
        'full_name': staff.user.full_name,
        'email': staff.user.email,
        'jabatan': staff.jabatan,
        'shift_kerja': staff.shift_kerja,
        'alamat': staff.alamat,
        'no_hp': staff.no_hp,
    }

    form = StaffForm(request.POST or None, initial=initial_data)

    if request.method == 'POST' and form.is_valid():
        try:
            data = form.cleaned_data
            user_data = {k: data[k] for k in ['username', 'full_name', 'email', 'password']}
            staff_data = {k: data[k] for k in ['jabatan', 'shift_kerja', 'alamat', 'no_hp']}
            StaffService.update_staff(id, user_data, staff_data)
            messages.success(request, f"Data staff {data['full_name']} berhasil diupdate.")
            return redirect('staff_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    context = {
        'form': form,
        'staff': staff,
        'page_title': 'Edit Staff',
        'breadcrumbs': [
            {'name': 'Manajemen staff', 'url': reverse('staff_index')},
            {'name': 'Edit staff', 'url': None},
        ],
        'jabatan_options' : [
            ('Administrasi', 'Administrasi'),
            ('Kasir', 'Kasir'),
            ('Apoteker', 'Apoteker'),
        ]
    }
    return render(request, 'pages/accounts/staff/edit.html', context)

@login_required
def staff_delete(request, id):
    try:
        StaffService.delete_staff(id)
        messages.success(request, "Data staff dan akun user berhasil dihapus.")
    except Staff.DoesNotExist:
        messages.error(request, "Staff tidak ditemukan.")
    except Exception as e:
        messages.error(request, f"Terjadi kesalahan: {str(e)}")
            
    return redirect('staff_index')
