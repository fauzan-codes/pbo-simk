from django.db import models
from django.utils.crypto import get_random_string

from accounts.models import TimestampModel

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