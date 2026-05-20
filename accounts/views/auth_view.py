from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import User, Pasien
from django.urls import reverse
from ..forms import PasienForm

def welcome_view(request):
    return render(request, 'pages/welcome.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'pages/auth/login.html', {
        'left_features': [
            'Rekam medis elektronik terintegrasi',
            'Manajemen stok obat & farmasi',
            'Laporan keuangan real-time',
            'Penjadwalan dokter & antrian pasien',
        ]
    })

def register_view(request): 
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        full_name   = request.POST.get('full_name', '').strip()
        username    = request.POST.get('username', '').strip()
        email   = request.POST.get('email', '').strip()
        password1   = request.POST.get('password1', '')
        password2   = request.POST.get('password2', '')

        nik = request.POST.get("nik")
        tanggal_lahir = request.POST.get('tanggal_lahir')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        no_hp = request.POST.get('no_hp')
        alamat = request.POST.get('alamat')

        if not all([full_name, username, email, password1, password2, nik, tanggal_lahir, jenis_kelamin, no_hp, alamat]):
            messages.error(request, 'Semua field wajib diisi.')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan, coba yang lain.')

        elif Pasien.objects.filter(nik=nik).exists():
            messages.error(request, 'Nik sudah digunakan, coba yang lain.')

        elif User.objects.filter(email=username).exists():
            messages.error(request, 'Email sudah digunakan, coba yang lain.')

        elif password1 != password2:
            messages.error(request, 'Konfirmasi password tidak cocok.')

        elif len(password1) < 8:
            messages.error(request, 'Password minimal 8 karakter.')

        else:
            user = User.objects.create_user(
                full_name=full_name,
                email=email,
                username=username,
                password=password1,
            )
            first_name, *last = full_name.split(' ', 1)
            user.first_name = first_name
            user.last_name  = last[0] if last else ''
            user.save()

            Pasien.objects.create(
                user = user,
                nik = nik,
                tanggal_lahir = tanggal_lahir,
                jenis_kelamin = jenis_kelamin,
                no_hp = no_hp,
                alamat = alamat
            )

            messages.success(request, f'Akun berhasil dibuat. Silakan masuk.')
            return redirect('login')
        
    jenis_kelamin_options = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]

    form = PasienForm(request.POST or None)
    context = {
        'left_features': [
            'Akses modul sesuai role pengguna',
            'Data tersimpan aman & terenkripsi',
            'Notifikasi real-time untuk staf',
            'Riwayat aktivitas tercatat otomatis',
        ],
        'jenis_kelamin_options': jenis_kelamin_options,
        'form' : form
    }

    return render(request, 'pages/auth/register.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Anda berhasil keluar.')
    return redirect('login')

def generate_superadmin(request):
    checkSuperadmin = User.objects.filter(role="admin")

    if checkSuperadmin:
        messages.error(request, "Akun superadmin sudah ada")
    else:
        User.objects.create_superuser(
            full_name = "Administrator SIMK",
            username = "superadmin",
            email = "admin@gmail.com",
            password = "password",
            role = "admin"
        )
        messages.success(request, "Akun superadmin berhasil dibuat")
    return redirect('login')

