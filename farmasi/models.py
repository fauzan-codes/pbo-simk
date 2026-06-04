from django.db import models
from django.utils import timezone
from accounts.models import TimestampModel

class KategoriObat(TimestampModel):
    nama_kategori = models.CharField(max_length=100)

    class Meta:
        db_table = 'kategori_obat'

class Obat(TimestampModel):
    nama_obat = models.CharField(max_length=255)
    kode_obat = models.CharField(max_length=20, unique=True)
    kategori = models.ForeignKey(KategoriObat, on_delete=models.CASCADE)
    satuan = models.CharField(max_length=20)
    stok = models.PositiveIntegerField()
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = TimestampModel.dibuat_pada
    updated_at = TimestampModel.diperbarui_pada

    def __generate_kode_obat(self):
        today_str = timezone.now().strftime('%Y%m%d')
        prefix = f"OBT-{today_str}-"
        
        last_obat = Obat.objects.filter(
            kode_obat__startswith=prefix
        ).order_by('-kode_obat').first()
        
        if last_obat:
            last_number = int(last_obat.kode_obat.split('-')[-1])
            new_number = str(last_number + 1).zfill(3)
        else:
            new_number = "001"
            
        return f"{prefix}{new_number}"

    def save(self, *args, **kwargs):
        if not self.kode_obat:
            self.kode_obat = self.__generate_kode_obat()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'obat'
    
    def save(self, *args, **kwargs):
        if not self.kode_obat:
            self.kode_obat = self.__generate_kode_obat()
        super().save(*args, **kwargs)

class Resep(TimestampModel):
    rekam_medis = models.ForeignKey('pelayanan.RekamMedis', on_delete=models.CASCADE)
    apoteker = models.ForeignKey('accounts.Staff', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='diproses')
    tanggal_resep = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resep'

class DetailResep(TimestampModel):
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE)
    obat = models.ForeignKey(Obat, on_delete=models.CASCADE)
    jumlah_diminta = models.PositiveIntegerField()
    dosis_aturan = models.CharField(max_length=100)
    subtotal_harga = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'detail_resep'