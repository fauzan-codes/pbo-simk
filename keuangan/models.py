from django.db import models

class Tagihan(models.Model):
    nomor_invoice = models.CharField(max_length=50, unique=True)
    kunjungan = models.OneToOneField('pelayanan.Kunjungan', on_delete=models.CASCADE)
    kasir = models.ForeignKey('accounts.Staff', on_delete=models.SET_NULL, null=True)
    total_biaya_tindakan = models.DecimalField(max_digits=12, decimal_places=2)
    total_biaya_obat = models.DecimalField(max_digits=12, decimal_places=2)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    metode_bayar = models.ForeignKey('master_data.MetodePembayaran', on_delete=models.SET_NULL, null=True)
    status_pembayaran = models.CharField(max_length=20, default='belum_lunas')
    waktu_pembayaran = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tagihan'