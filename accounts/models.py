from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from datetime import datetime

class TimestampModel(models.Model):
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUserManager(BaseUserManager):
    def create_user(self, full_name, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, username=username, email=email, **extra_fields)
        
        user.set_password(password) 
        user.save(using=self._db)
        return user

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

class BaseUserProfile(TimestampModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='%(class)s_profile' 
    )
    no_hp = models.CharField(max_length=15)
    alamat = models.TextField()

    class Meta:
        abstract = True

    def get_identitas(self):
        pass

class Dokter(BaseUserProfile):
    spesialisasi = models.CharField(max_length=100)
    nomor_sip = models.CharField(max_length=50)
    tarif_jasa = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'dokter'

    def get_identitas(self):
        return f"{self.user.full_name} (Dokter {self.spesialisasi})"

class Staff(BaseUserProfile):
    jabatan = models.CharField(max_length=50)
    shift_kerja = models.CharField(max_length=50)

    class Meta:
        db_table = 'staff'

    def get_identitas(self):
        return f"{self.user.full_name} ({self.jabatan})"

class Pasien(BaseUserProfile):
    nomor_rekam_medis = models.CharField(max_length=20, unique=True)
    nik = models.CharField(max_length=20, unique=True)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=10, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])

    class Meta:
        db_table = 'pasien'

    def get_identitas(self):
        return f"{self.nomor_rekam_medis} - {self.user.full_name}"

    def save(self, *args, **kwargs):
        if not self.nomor_rekam_medis:
            self.nomor_rekam_medis = self._generate_nomor_rm()
        
        super().save(*args, **kwargs)

    @classmethod
    def _generate_nomor_rm(cls):
        today_str = datetime.now().strftime('%Y%m%d')
        prefix = f"RM-{today_str}-"
        
        last_pasien = cls.objects.filter(
            nomor_rekam_medis__startswith=prefix
        ).order_by('-nomor_rekam_medis').first()
        
        if last_pasien:
            last_number = int(last_pasien.nomor_rekam_medis.split('-')[-1])
            new_number = str(last_number + 1).zfill(3)
        else:
            new_number = "001"
            
        return f"{prefix}{new_number}"

