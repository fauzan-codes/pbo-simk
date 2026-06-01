from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from administrasi.models import Tiket

@login_required
def dashboard_view(request):
    user = request.user

    if not messages.get_messages(request):
        messages.info(request, f"Selamat datang kembali, {user.full_name}! Ini adalah dashboard {user.get_role_display()} Anda.")

    name_parts = user.full_name.split()
    if len(name_parts) >= 2:
        initials = (name_parts[0][0] + name_parts[1][0]).upper()
    elif len(name_parts) == 1:
        initials = name_parts[0][:2].upper()
    else:
        initials = "U"

    role_detail = None
    quick_links = []

    if user.role == 'pasien':
        role_detail = getattr(user, 'pasien_profile', None)
        quick_links = [
            {'title': 'Buat Janji Temu', 'desc': 'Daftar Online', 'url': reverse('daftar_online_index'), 'color': 'text-blue-600 bg-blue-100'},
            {'title': 'Riwayat Medis', 'desc': 'Lihat hasil periksa', 'url': '#', 'color': 'text-emerald-600 bg-emerald-100'},
            {'title': 'Tagihan', 'desc': 'Status pembayaran', 'url': '#', 'color': 'text-amber-600 bg-amber-100'},
        ]
    
    elif user.role == 'dokter':
        role_detail = getattr(user, 'dokter_profile', None)
        quick_links = [
            {'title': 'Mulai Pemeriksaan', 'desc': 'Buka daftar antrean', 'url': reverse('rawat_pasien_index'), 'color': 'text-indigo-600 bg-indigo-100'},
            {'title': 'Jadwal Praktik', 'desc': 'Atur jam kerja', 'url': reverse('jadwal_praktik_index'), 'color': 'text-purple-600 bg-purple-100'},
        ]
        
    elif user.role in ['staff', 'admin']:
        role_detail = getattr(user, 'staff_profile', None) 
        quick_links = [
            {'title': 'Modul Administrasi', 'desc': 'Pendaftaran pasien', 'url': reverse('check_in_index'), 'color': 'text-rose-600 bg-rose-100'},
            {'title': 'Modul Kasir', 'desc': 'Kelola pembayaran', 'url': '#', 'color': 'text-green-600 bg-green-100'},
            {'title': 'Modul Apoteker', 'desc': 'Kelola stok obat', 'url': reverse('stok_obat_index'), 'color': 'text-cyan-600 bg-cyan-100'},
        ]

    context = {
        'breadcrumbs': [{'name': 'Dashboard', 'url': reverse('dashboard')}],
        'page_title': 'Dashboard',
        'user_data': user,
        'role_detail': role_detail,
        'initials': initials,
        'quick_links': quick_links
    }

    if user.role == "pasien":
        context['list_tiket'] = Tiket.objects.filter(pasien=user.pasien_profile)

    return render(request, 'pages/dashboard/index.html', context)


