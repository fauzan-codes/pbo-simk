from django.db import models
from accounts.models import TimestampModel

class TindakanMedis(TimestampModel):
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
    
class Kunjungan(TimestampModel):
    pasien = models.ForeignKey('accounts.Pasien', on_delete=models.CASCADE)
    jadwal = models.ForeignKey('administrasi.JadwalPraktik', on_delete=models.CASCADE)
    tanggal_kunjungan = models.DateField()
    nomor_antrean = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='diproses')

    class Meta:
        db_table = 'kunjungan'

    @classmethod
    def generateNomorAntrean(cls, jadwal, tanggal_kunjungan):
        last_instance = cls.objects.filter(
            tanggal_kunjungan=tanggal_kunjungan,
            jadwal__poli=jadwal.poli
        ).order_by('nomor_antrean').last()

        return last_instance.nomor_antrean + 1 if last_instance else 1
    
    @classmethod
    def changeStatus(cls, kunjungan_id, status_baru):
        return cls.objects.filter(id=kunjungan_id).update(status=status_baru)

    @property
    def kode_antrean(self):
        if self.jadwal and self.jadwal.poli and self.nomor_antrean:
            kode_poli = self.jadwal.poli.kode_poli
            return f"{kode_poli}{str(self.nomor_antrean).zfill(3)}"
        return "N/A"
        

class RekamMedis(TimestampModel):
    kunjungan = models.OneToOneField(Kunjungan, on_delete=models.CASCADE)
    keluhan = models.TextField()
    diagnosa = models.TextField()
    tekanan_darah = models.CharField(max_length=20)
    suhu_tubuh = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    class Meta:
        db_table = 'rekam_medis'

class TindakanRekamMedis(TimestampModel):
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE)
    tindakan_medis = models.ForeignKey('pelayanan.TindakanMedis', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tindakan_rekam_medis'




