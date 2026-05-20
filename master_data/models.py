from django.db import models
from pelayanan.models import Kunjungan

class Poli(models.Model):
    kode_poli = models.CharField(max_length=10, unique=True)
    nama_poli = models.CharField(max_length=100)

    class Meta:
        db_table = 'poli'

class JadwalPraktik(models.Model):
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
    
class TindakanMedis(models.Model):
    kode_tindakan = models.CharField(max_length=10, unique=True, blank=True)
    nama_tindakan = models.CharField(max_length=100)
    tarif = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'tindakan_medis'
    
    def save(self, *args, **kwargs):
        if not self.kode_tindakan:
            self.kode_tindakan = self.generate_kode_tindakan()
            
        super(TindakanMedis, self).save(*args, **kwargs)

    @classmethod
    def generate_kode_tindakan(cls):
        prefix = "TND-"
        
        last_instance = cls.objects.all().order_by('-id').first()
        
        if last_instance and last_instance.kode_tindakan:
            try:
                last_number = int(last_instance.kode_tindakan.split('-')[1])
                new_number = last_number + 1
            except (IndexError, ValueError):
                new_number = 1
        else:
            new_number = 1
            
        return f"{prefix}{str(new_number).zfill(4)}"

    def __str__(self):
        return f"{self.kode_tindakan} - {self.nama_tindakan}"
    
class MetodePembayaran(models.Model):
    nama_metode = models.CharField(max_length=50)

    class Meta:
        db_table = 'metode_pembayaran'