# pelayanan/models.py
from django.db import models

class Kunjungan(models.Model):
    pasien = models.ForeignKey('accounts.Pasien', on_delete=models.CASCADE)
    jadwal = models.ForeignKey('master_data.JadwalPraktik', on_delete=models.CASCADE)
    tanggal_kunjungan = models.DateField()
    nomor_antrean = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='menunggu')

    class Meta:
        db_table = 'kunjungan'

class RekamMedis(models.Model):
    kunjungan = models.OneToOneField(Kunjungan, on_delete=models.CASCADE)
    keluhan = models.TextField()
    diagnosa = models.TextField()
    tekanan_darah = models.CharField(max_length=20)
    suhu_tubuh = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        db_table = 'rekam_medis'

class TindakanRekamMedis(models.Model):
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE)
    tindakan_medis = models.ForeignKey('master_data.TindakanMedis', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tindak_rekam_medis'