from django.db import models

class KategoriObat(models.Model):
    nama_kategori = models.CharField(max_length=100)

class Obat(models.Model):
    kode_obat = models.CharField(max_length=10, unique=True)
    kategori = models.ForeignKey(KategoriObat, on_delete=models.CASCADE)
    satuan = models.CharField(max_length=20)
    stok = models.PositiveIntegerField()
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'obat'

class Resep(models.Model):
    rekam_medis = models.ForeignKey('pelayanan.RekamMedis', on_delete=models.CASCADE)
    apoteker = models.ForeignKey('accounts.Staff', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='diproses')
    tanggal_resep = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resep'

class DetailResep(models.Model):
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE)
    obat = models.ForeignKey(Obat, on_delete=models.CASCADE)
    jumlah_diminta = models.PositiveIntegerField()
    dosis_aturan = models.CharField(max_length=100)
    subtotal_harga = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'detail_resep'