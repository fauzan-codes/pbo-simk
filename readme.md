# SISTEM INFORMASI MANAJEMEN KLINIK (SIMK)

## 📋 Deskripsi Project

Sistem Informasi Manajemen Klinik (SIMK) adalah aplikasi berbasis web yang dibangun menggunakan **Django** dan **Tailwind CSS** untuk mengelola operasional klinik. Sistem ini memungkinkan manajemen data pasien, rekam medis, administrasi klinik, data obat farmasi, data tagihan, dan layanan pelayanan kesehatan dalam satu platform. Live demo bisa diakses di [link website](https://simk.ardiansyahdheva.my.id).

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

### 4. **Farmasi**
   - Manajemen kategori obat
   - Manajemen stok obat
   - Konfirmasi resep dokter

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

## 📸 Screenshot & Fitur Per Role

### 🔓 Guest (Belum Login)
| | |
|---|---|
| ![Guest 1](screenshoot/guest/1.png) | ![Guest 2](screenshoot/guest/2.png) |
| ![Guest 3](screenshoot/guest/3.png) | |

**Fitur:** Halaman landing, login, register

---

### 👤 Pasien
| | |
|---|---|
| ![Pasien 1](screenshoot/pasien/1.png) | ![Pasien 2](screenshoot/pasien/2.png) |
| ![Pasien 3](screenshoot/pasien/3.png) | |

**Fitur:** Dashboard pasien, daftar online, generate tiket

---

### 👨‍💼 Staff Administrasi
| | |
|---|---|
| ![Staff Admin 1](screenshoot/staff/administrasi/1.png) | ![Staff Admin 2](screenshoot/staff/administrasi/2.png) |
| ![Staff Admin 3](screenshoot/staff/administrasi/3.png) | ![Staff Admin 4](screenshoot/staff/administrasi/4.png) |
| ![Staff Admin 5](screenshoot/staff/administrasi/5.png) | ![Staff Admin 6](screenshoot/staff/administrasi/6.png) |
| ![Staff Admin 7](screenshoot/staff/administrasi/7.png) | ![Staff Admin 8](screenshoot/staff/administrasi/8.png) |

**Fitur:** Manajemen loket, check-in pasiean, tiket antrean

---

### 👨‍⚕️ Dokter
| | |
|---|---|
| ![Dokter 1](screenshoot/dokter/1.png) | ![Dokter 2](screenshoot/dokter/2.png) |
| ![Dokter 3](screenshoot/dokter/3.png) | ![Dokter 4](screenshoot/dokter/4.png) |
| ![Dokter 5](screenshoot/dokter/5.png) | |

**Fitur:** Manajemen tindakan, input form pelayanan, buat resep obat

---

### 💊 Staff Apoteker
| | |
|---|---|
| ![Apoteker 1](screenshoot/staff/apoteker/1.png) | ![Apoteker 2](screenshoot/staff/apoteker/2.png) |
| ![Apoteker 3](screenshoot/staff/apoteker/3.png) | ![Apoteker 4](screenshoot/staff/apoteker/4.png) |![Apoteker 5](screenshoot/staff/apoteker/5.png) | |

**Fitur:** Kelola kategori obat, kelola stok obat, konfirmasi resep dokter

---

### 💰 Staff Kasir
| | |
|---|---|
| ![Kasir 1](screenshoot/staff/kasir/1.png) | ![Kasir 2](screenshoot/staff/kasir/2.png) |
| ![Kasir 3](screenshoot/staff/kasir/3.png) | ![Kasir 4](screenshoot/staff/kasir/4.png) |
| ![Kasir 5](screenshoot/staff/kasir/5.png) | |

**Fitur:** Kelola metode pembayaran, generate invoice, riwayat transaksi

---

### 🧑‍💼 Admin
| | |
|---|---|
| ![Admin 1](screenshoot/admin/1.png) | ![Admin 2](screenshoot/admin/2.png) |
| ![Admin 3](screenshoot/admin/3.png) | ![Admin 4](screenshoot/admin/4.png) |
| ![Admin 5](screenshoot/admin/5.png) | ![Admin 6](screenshoot/admin/6.png) |

**Fitur:** Manajemen user, poli, jadwal

---
