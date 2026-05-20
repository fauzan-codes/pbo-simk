from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from datetime import datetime

class CustomUserManager(BaseUserManager):
    def create_user(self, full_name, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, username=username, email=email, **extra_fields)
        
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(full_name, username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('staff', 'Staff'),
        ('dokter', 'Dokter'),
        ('pasien', 'Pasien'),
    )

    full_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='pasien')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'user'

class Dokter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dokter_profile')
    spesialisasi = models.CharField(max_length=100)
    nomor_sip = models.CharField(max_length=50)
    tarif_jasa = models.DecimalField(max_digits=12, decimal_places=2)
    no_hp = models.CharField(max_length=5)
    alamat = models.TextField()

    class Meta:
        db_table = 'dokter'

class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    jabatan = models.CharField(max_length=50)
    shift_kerja = models.CharField(max_length=50)
    no_hp = models.CharField(max_length=5)
    alamat = models.TextField()

    class Meta:
        db_table = 'staff'

class Pasien(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='pasien_profile')
    nomor_rekam_medis = models.CharField(max_length=20, unique=True)
    nik = models.CharField(max_length=20, unique=True)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=10, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    alamat = models.TextField()
    no_hp = models.CharField(max_length=15)

    class Meta:
        db_table = 'pasien'

    def save(self, *args, **kwargs):
        if not self.nomor_rekam_medis:
            self.nomor_rekam_medis = self.generate_nomor_rm()
        
        super().save(*args, **kwargs)

    @classmethod
    def generate_nomor_rm(cls):
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

