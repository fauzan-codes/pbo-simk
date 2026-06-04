from django.db import models
from django.utils.crypto import get_random_string
from pelayanan.models import Kunjungan

from accounts.models import TimestampModel

class Poli(TimestampModel):
    kode_poli = models.CharField(max_length=10, unique=True)
    nama_poli = models.CharField(max_length=100)

    class Meta:
        db_table = 'poli'

    # Pemanggilan str(poli) untuk format nama_poli(kode_poli)
    def __str__(self):
        return f"{self.nama_poli} (Kode: {self.kode_poli})"

class JadwalPraktik(TimestampModel):
    dokter = models.ForeignKey('accounts.Dokter', on_delete=models.CASCADE)
    poli = models.ForeignKey(Poli, on_delete=models.CASCADE)
    hari = models.CharField(max_length=20)
    jam_mulai = models.TimeField() 
    jam_selesai = models.TimeField()

    class Meta:
        db_table = 'jadwal_praktik'

    # Property kombinasi hari, jam mulai, jam selesai
    @property
    def jadwal_lengkap(self):
        return f"{self.hari} ({self.jam_mulai.strftime('%H:%M')} - {self.jam_selesai.strftime('%H:%M')})"

    def __str__(self):
        return f"{self.dokter.user.full_name} | {self.jadwal_lengkap}"

    # Method untuk mendapat antrian pasien per jadwal (belum diterapkan)
    @classmethod
    def get_jadwal_unavailable(cls):
        jadwal_sibuk = Kunjungan.objects.filter(
            status='diproses'
        ).values_list('jadwal_id', flat=True).distinct()
        return list(jadwal_sibuk)

class Tiket(TimestampModel):
    no_tiket = models.CharField(max_length=20, unique=True)
    pasien = models.ForeignKey('accounts.Pasien', on_delete=models.CASCADE)
    kunjungan = models.ForeignKey('pelayanan.Kunjungan', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tiket'

    def __str__(self):
        return f"Tiket: {self.no_tiket} - {self.pasien.user.full_name}"

    def save(self, *args, **kwargs):
        if not self.no_tiket:
            self.no_tiket = self.__generate_no_tiket()
        
        super().save(*args, **kwargs)

    def __generate_no_tiket(self):
        prefix = "TK-"
        panjang_acak = 8 
        
        while True:
            karakter_acak = get_random_string(
                length=panjang_acak, 
                allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            )
            
            hasil_tiket = f"{prefix}{karakter_acak}"
            
            if not Tiket.objects.filter(no_tiket=hasil_tiket).exists():
                return hasil_tiket
            

class Loket(TimestampModel):
    nama_loket = models.CharField(max_length=255, unique=True)
    staff = models.ForeignKey('accounts.Staff', on_delete=models.SET_NULL, null=True)
    kunjungan = models.ForeignKey('pelayanan.Kunjungan', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'loket'

    def __str__(self):
        nama_petugas = self.staff.user.full_name if self.staff else "Kosong"
        return f"{self.nama_loket} (Petugas: {nama_petugas})"