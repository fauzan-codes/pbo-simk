from django.db import models

class Poli(models.Model):
    kode_poli = models.CharField(max_length=10, unique=True)
    nama_poli = models.CharField(max_length=100)

class JadwalPraktik(models.Model):
    dokter = models.ForeignKey('accounts.Dokter', on_delete=models.CASCADE)
    poli = models.ForeignKey(Poli, on_delete=models.CASCADE)
    hari = models.CharField(max_length=20)
    jam_mulai = models.TimeField() 
    jam_selesai = models.TimeField()

    

class TindakanMedis(models.Model):
    kode_tindakan = models.CharField(max_length=10, unique=True)
    nama_tindakan = models.CharField(max_length=100)
    tarif = models.DecimalField(max_digits=12, decimal_places=2)
    def save(self, *args, **kwargs):
        if not self.kode_tindakan:
            prefix = "TND-"
            last_instance = TindakanMedis.objects.all().order_by('id').last()
            if last_instance:
                last_number = int(last_instance.kode_tindakan.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            self.kode_tindakan = f"{prefix}{str(new_number).zfill(4)}"
        super(TindakanMedis, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.kode_tindakan} - {self.nama_tindakan}"

class MetodePembayaran(models.Model):
    nama_metode = models.CharField(max_length=50)