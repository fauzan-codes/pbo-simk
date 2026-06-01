from django.db import models
from django.utils.crypto import get_random_string
from pelayanan.models import Kunjungan

from accounts.models import TimestampModel

class Poli(TimestampModel):
    kode_poli = models.CharField(max_length=10, unique=True)
    nama_poli = models.CharField(max_length=100)

    class Meta:
        db_table = 'poli'

class JadwalPraktik(TimestampModel):
    dokter = models.ForeignKey('accounts.Dokter', on_delete=models.CASCADE)
    poli = models.ForeignKey(Poli, on_delete=models.CASCADE)
    hari = models.CharField(max_length=20)
    jam_mulai = models.TimeField() 
    jam_selesai = models.TimeField()

    class Meta:
        db_table = 'jadwal_praktik'

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

    def save(self, *args, **kwargs):
        if not self.no_tiket:
            self.no_tiket = self._generate_no_tiket()
        
        super().save(*args, **kwargs)

    @classmethod
    def _generate_no_tiket(cls):
        prefix = "TK-"
        panjang_acak = 8 
        
        while True:
            karakter_acak = get_random_string(
                length=panjang_acak, 
                allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            )
            
            hasil_tiket = f"{prefix}{karakter_acak}"
            
            if not cls.objects.filter(no_tiket=hasil_tiket).exists():
                return hasil_tiket
            

class Loket(TimestampModel):
    nama_loket = models.CharField(max_length=255, unique=True)
    staff = models.ForeignKey('accounts.Staff', on_delete=models.SET_NULL, null=True)
    kunjungan = models.ForeignKey('pelayanan.Kunjungan', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'loket'