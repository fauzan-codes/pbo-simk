# SISTEM INFORMASI MANAJEMEN KLINIK (SIMK)

## 📋 Deskripsi Project

Sistem Informasi Manajemen Klinik (SIMK) adalah aplikasi berbasis web yang dibangun menggunakan **Django** dan **Tailwind CSS** untuk mengelola operasional klinik secara menyeluruh. Sistem ini memungkinkan manajemen data pasien, rekam medis, administrasi klinik, data obat farmasi, data keuangan, dan layanan pelayanan kesehatan dalam satu platform terpadu.

## 👥 Anggota Kelompok

| No | Nama | NIM | Peran |
|----|------|-----|-------|
| 1 | Ardiansyah Dhevashidqi Madany | 25051204072 | Modul Administrasi |
| 2 | Fauzan Adhim Muntazhar | 25051204003 | Modul Pelayanan |
| 3 | Ernesta Wardanto | 25051204158 | Modul Farmasi |
| 4 | Nur Javier Prasetyo | 25051204002 | Modul Keuangan |

## ⭐ Fitur Utama

### 1. **Manajemen Akun & Autentikasi**
   - Login, Register & Logout
   - Manajemen akun staff, dokter, & pasien
   - Pembatasan hak akses berdasarkan role

### 2. **Administrasi**
   - Manajemen poli
   - Manajemen jadwal praktik
   - Manajemen loket
   - Sistem tiket & antrean pasien

### 3. **Pelayanan**
   - Manajemen tindakan
   - Form pelayanan dokter 
   - Resep obat
   - Riwayat tindakan pasien

### 4. **Farmasi**
   - Manajemen kategori obat
   - Manajemen stok obat
   - Konfirmasi resep dokter
   - Riwayat resep obat

### 5. **Keuangan**
   - Manajemen metode pembayaran
   - Pembayaran tagihan pasien
   - Generate Invoice pembayaran
   - Riwayat pembayaran pasien


## 🚀 Cara Menjalankan Project

### Prasyarat
- Python 3.13+
- Virtual Environment (venv)
- Django

### Langkah-Langkah Setup

#### 1. Setup Awal Project
```bash
./setup.bat
```
Script ini akan menginstal semua dependency yang diperlukan.

#### 2. Menjalankan Server
```bash
./run.bat
```
Perintah ini akan menjalankan Django server dan Tailwind CSS watcher secara bersamaan.

#### 3. Fresh Migrate Database (opsional)
Jika perlu reset database dan membuat fresh database:
```bash
# Pastikan venv sudah aktif
py fresh_migrate.py
```

#### 4. Menjalankan Data Seeder
Untuk mengisi database dengan data testing:
```bash
# Pastikan venv sudah aktif
py manage.py seed --clear
```

#### 5. Akses Aplikasi
```
http://localhost:8000
```

**Catatan:** Credential login untuk testing dapat diakses di file `login_credentials.txt`

## 🏗️ Implementasi OOP (Object-Oriented Programming)

*Dokumentasi implementasi OOP akan ditambahkan setelah dilakukan perbaikan penerapan PBO pada model.*

---

## 📸 Screenshot Tampilan Program

### Halaman Login
![Login Page](static/screenshots/login.png)

*Screenshot akan ditambahkan kemudian*

---
