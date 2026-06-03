from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from datetime import datetime

# Master class pencatatan waktu (dipakai di semua class)
class TimestampModel(models.Model):
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



# Class untuk handle custom create_user
class CustomUserManager(BaseUserManager):
    def create_user(self, full_name, username, email, password=None, **extra_fields):
        # Normalisasi email ke lower case
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, username=username, email=email, **extra_fields)
        
        # Set password supaya di hash dulu sebelum disimpan ke database
        user.set_password(password) 
        user.save(using=self._db)
        return user
    


# Class user untuk login (semua role pakai class ini)
class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('dokter', 'Dokter'),
        ('pasien', 'Pasien'),
    )

    full_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='pasien')

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'user'



# Master class untuk identitas user
class BaseUserProfile(TimestampModel):
    # Relasi ke tabel user
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        # Pemanggilan relasi user ke class masing masing role (cnth: dokter_profile, staff_profile, dokter_profile)
        related_name='%(class)s_profile' 
    )
    no_hp = models.CharField(max_length=15)
    alamat = models.TextField()

    class Meta:
        abstract = True

    # method abstrak harus di terapkan di semua subclass
    def get_identitas(self):
        raise NotImplementedError(f"{self.__class__.__name__} harus implement get_identitas()")
    
    def _format_no_hp(self):
        if self.no_hp.startswith('0'):
            self.no_hp = '+62' + self.no_hp[1:]
        elif self.no_hp.startswith('8'):
            self.no_hp = '+62' + self.no_hp

    def save(self, *args, **kwargs):
        self._format_no_hp()
        super().save(*args, **kwargs)



# class untuk profil user dengan role dokter
class Dokter(BaseUserProfile):
    spesialisasi = models.CharField(max_length=100)
    nomor_sip = models.CharField(max_length=50)
    tarif_jasa = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'dokter'

    def get_identitas(self):
        return f"{self.user.full_name} (Dokter {self.spesialisasi})"
    


# class untuk profil user dengan role staff
class Staff(BaseUserProfile):
    jabatan = models.CharField(max_length=50)
    shift_kerja = models.CharField(max_length=50)

    class Meta:
        db_table = 'staff'

    def get_identitas(self):
        return f"{self.user.full_name} ({self.jabatan})"
    


# class untuk profil user dengan role pasien
class Pasien(BaseUserProfile):
    nomor_rekam_medis = models.CharField(max_length=20, unique=True)
    nik = models.CharField(max_length=20, unique=True)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=10, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])

    class Meta:
        db_table = 'pasien'

    def get_identitas(self):
        return f"{self.nomor_rekam_medis} - {self.user.full_name}"
    
    @property
    def umur(self):
        import datetime
        today = datetime.date.today()
        return today.year - self.tanggal_lahir.year - (
            (today.month, today.day) < (self.tanggal_lahir.month, self.tanggal_lahir.day)
        )

    # override method class model untuk mengisi otomatis nomor_rekam_medis saat save/create pasien
    def save(self, *args, **kwargs):
        if not self.nomor_rekam_medis:
            self.nomor_rekam_medis = self.__generate_nomor_rm()
        
        super().save(*args, **kwargs)

    # Method private dipanggil ketika pembuatan user baru
    def __generate_nomor_rm(self):
        # Format nomor_rm prefix(RM-tanggal hari ini) + jumlah pasien yg daftar hari ini
        today_str = datetime.now().strftime('%Y%m%d')
        prefix = f"RM-{today_str}-"
        
        last_pasien = Pasien.objects.filter(
            nomor_rekam_medis__startswith=prefix
        ).order_by('-nomor_rekam_medis').first()
        
        if last_pasien:
            last_number = int(last_pasien.nomor_rekam_medis.split('-')[-1])
            new_number = str(last_number + 1).zfill(3)
        else:
            new_number = "001"
            
        return f"{prefix}{new_number}"

