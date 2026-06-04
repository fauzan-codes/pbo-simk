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
   1)	Sistem login dan registrasi pengguna
   2)	Manajemen data pasien, dokter, staff (create, read, update, delete)
   3)	Pembatasan hak akses berdasarkan role
   4)	Halaman dashboard setiap role

### 2. **Administrasi**
   1)	Pendaftaran online: Pasien dapat mendaftar secara online
   2)	Check-in: proses check-in pasien (online & offline)
   3)	Manajemen data loket (create, read, update, delete)
   4)	Sistem antrean dan pemanggilan pasien berdasarkan antrean
   5)	Display monitor untuk menampilkan antrean saat ini

### 3. **Pelayanan**
   1)	Manajemen data tindakan (create, read, update, delete)
   2)	Form Pelayanan: input data keluhan & diagnosa
   3)	Pembuatan resep obat: input data obat


### 4. **Farmasi**
   1)	Manajement kategori obat (create, read, update, delete)
   2)	Manajemen stok obat (create, read, update, delete)
   3)	Konfirmasi dan validasi resep dari dokter


### 5. **Keuangan**
   1)	Manajemen metode pembayaran (create, read, update, delete)
   2)	Create data tagihan pasien (generate invoice)
   3)	Riwayat pembayaran pasien


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

Sistem SIMK menerapkan prinsip-prinsip Object-Oriented Programming dalam desain model data Django. Berikut penjelasan implementasinya:

### 1. **Inheritance (Pewarisan)**

#### a. Model Abstrak Superclass - `TimestampModel`
Model abstrak yang digunakan sebagai base class untuk sebagian besar model dalam sistem:
```python
class TimestampModel(models.Model):
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```
- Semua model (Poli, JadwalPraktik, Tiket, Loket, TindakanMedis, Kunjungan, dll) mewarisi dari `TimestampModel`
- Memberikan catatan waktu otomatis untuk setiap entitas yang dibuat atau diperbarui

#### b. Hirarki User Profile
Hierarki inheritance untuk profil pengguna di `accounts/models.py`:
```python
class UserProfileModel(TimestampModel): # Superclass

class Dokter(UserProfileModel):# Subclass
class Staff(UserProfileModel): # Subclass  
class Pasien(UserProfileModel):# Subclass
```
- Setiap role memiliki atribut unik (spesialisasi dokter, jabatan staff, nomor rekam medis pasien)
- Implementasi polymorphism melalui method override `get_identitas()` di setiap subclass

#### c. Medical Record Base - `BaseMedicalRecord`
Abstract base class untuk records medis di `pelayanan/models.py`:
```python
class BaseMedicalRecord(TimestampModel):
    def validate_data(self):
        raise NotImplementedError('Subclass harus mengimplementasikan validate_data()')

class RekamMedis(BaseMedicalRecord):
    # Mengimplementasikan validate_data()
```

### 2. **Polymorphism (Polimorfisme)**

#### a. Workflow Pattern dengan Polymorphism
Implementasi polymorphism dalam status workflow (`pelayanan/models.py`):
```python
class StatusWorkflow: # Superclass
    def next_status(self): # Method Abstrak (harus implementasi pada subclass)
        raise NotImplementedError

class DiprosesWorkflow(StatusWorkflow): # Override method 
    def next_status(self):
        return 'rawat'

class RawatWorkflow(StatusWorkflow):    # Override method 
    def next_status(self):
        return 'resep'

class ResepWorkflow(StatusWorkflow):    # Override method 
    def next_status(self):
        return 'selesai'
```
- Model `Kunjungan` menggunakan workflow yang sesuai dengan status:
```python
def get_workflow(self):
    workflows = {
        self.STATUS_DIPROSES: DiprosesWorkflow(),
        self.STATUS_RAWAT: RawatWorkflow(),
        self.STATUS_RESEP: ResepWorkflow(),
    }
    return workflows.get(self.status)

def move_next_status(self):
    workflow = self.get_workflow()
    if workflow:
        self.status = workflow.next_status()
        self.save()
```

#### b. Method Override
Setiap subclass override method `get_identitas()` dengan implementasi unik:
```python
class UserProfileModel(TimestampModel):
    # Method abstrak (harus di implementasikan oleh subclass)
    def get_identitas(self):
        raise NotImplementedError(f"{self.__class__.__name__} harus implementasi _get_identitas()")

class Dokter(UserProfileModel):
    # Override oleh subclass dokter
    def get_identitas(self):
        return f"{self.user.full_name} (Dokter {self.spesialisasi})"

class Staff(UserProfileModel):
    # Override oleh subclass staff
    def get_identitas(self):
        return f"{self.user.full_name} ({self.jabatan})"

class Pasien(UserProfileModel):
    # Override oleh subclass pasien
    def get_identitas(self):
        return f"{self.nomor_rekam_medis} - {self.user.full_name}")
    

```
- Dokter: menampilkan nama + spesialisasi
- Staff: menampilkan nama + jabatan
- Pasien: menampilkan nomor rekam medis + nama

### 3. **Encapsulation (Enkapsulasi)**

#### a. Manager Pattern - `KunjunganManager`
Encapsulation logic database query dalam custom manager (`pelayanan/models.py`):
```python
class KunjunganManager(models.Manager):
    def antrean_dokter(self, dokter):
        return self.select_related(...).filter(jadwal__dokter=dokter)
    
    def antrean_rawat(self, dokter):
        return self.antrean_dokter(dokter).filter(status__in=['diproses', 'rawat', 'resep'])
```
- Menyembunyikan kompleksitas query logic
- Memberikan interface yang clean dan reusable

#### b. Private Methods
Penggunaan private methods (prefix `__`) untuk operasi internal:

```python
def __generate_kode_obat(self):
    today_str = timezone.now().strftime('%Y%m%d')
    prefix = f"OBT-{today_str}-"
    
    last_obat = Obat.objects.filter(
        kode_obat__startswith=prefix
    ).order_by('-kode_obat').first()
    
    if last_obat:
        last_number = int(last_obat.kode_obat.split('-')[-1])
        new_number = str(last_number + 1).zfill(3)
    else:
        new_number = "001"
        
    return f"{prefix}{new_number}"
```

- `Pasien.__generate_nomor_rm()` - generate nomor rekam medis
- `Tiket.__generate_no_tiket()` - generate nomor tiket
- `TindakanMedis.__generate_kode_tindakan()` - generate kode tindakan
- `Obat.__generate_kode_obat()` - generate kode obat
- `Tagihan.__generate_nomor_invoice()` - generate nomor invoice

#### c. Auto-Formatting pada Save
Method `save()` di `UserProfileModel` untuk auto-format nomor HP:
```python
def _format_no_hp(self): # Protected Method
    if self.no_hp.startswith('0'):
        self.no_hp = '+62' + self.no_hp[1:]

def save(self, *args, **kwargs):
    self._format_no_hp()
    super().save(*args, **kwargs)
```

### 4. **Abstraction (Abstraksi)**

#### a. Abstract Base Classes
```python
# Mencegah django membuat otomatis object migrasi ke database
 class Meta:
    abstract = True
```

- `TimestampModel` - abstraksi untuk timestamp fields
- `UserProfileModel` - abstraksi untuk profil pengguna
- `BaseMedicalRecord` - abstraksi untuk validasi medical records

#### b. Property Decorators
Mengabstraksi logic kompleks sebagai property sederhana:
```python
@property
def umur(self):  # Pasien model
    # Menghitung umur dari tanggal_lahir
    
@property
def kode_antrean(self):  # Kunjungan model
    # generate kode antrean dari poli + nomor antrean
    
@property
def jadwal_lengkap(self):  # JadwalPraktik model
    # Format jadwal lengkap hari + jam_mulai + jam_selesai
```

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
| ![Apoteker 3](screenshoot/staff/apoteker/3.png) | ![Apoteker 4](screenshoot/staff/apoteker/4.png) 
| ![Apoteker 5](screenshoot/staff/apoteker/5.png) | |

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
