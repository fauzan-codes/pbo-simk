from django.db import models
from django.utils import timezone

from accounts.models import TimestampModel

class MetodePembayaran(TimestampModel):
    nama_metode = models.CharField(max_length=50)

    class Meta:
        db_table = 'metode_pembayaran'

class Tagihan(TimestampModel):
    nomor_invoice = models.CharField(max_length=50, unique=True)
    kunjungan = models.OneToOneField('pelayanan.Kunjungan', on_delete=models.CASCADE)
    kasir = models.ForeignKey('accounts.Staff', on_delete=models.SET_NULL, null=True)
    total_biaya_tindakan = models.DecimalField(max_digits=12, decimal_places=2)
    total_biaya_obat = models.DecimalField(max_digits=12, decimal_places=2)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    metode_bayar = models.ForeignKey('keuangan.MetodePembayaran', on_delete=models.SET_NULL, null=True)
    status_pembayaran = models.CharField(max_length=20, default='belum_lunas')
    waktu_pembayaran = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tagihan'

    def save(self, *args, **kwargs):
        if not self.nomor_invoice:
            self.nomor_invoice = self.__generate_nomor_invoice()
        super().save(*args, **kwargs)

    @classmethod
    def __generate_nomor_invoice(cls):
        # Format: INV-20260530-0001
        hari_ini = timezone.now().date()
        tanggal_str = hari_ini.strftime('%Y%m%d')
        prefix = f"INV-{tanggal_str}-"

        last_invoice = cls.objects.filter(nomor_invoice__startswith=prefix).order_by('-nomor_invoice').first()

        if last_invoice:
            try:
                last_sequence = int(last_invoice.nomor_invoice.split('-')[-1])
                new_sequence = last_sequence + 1
            except (IndexError, ValueError):
                new_sequence = 1
        else:
            new_sequence = 1

        return f"{prefix}{str(new_sequence).zfill(4)}"
