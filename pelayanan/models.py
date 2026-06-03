from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import TimestampModel


class BaseMedicalRecord(TimestampModel):
    class Meta:
        abstract = True

    def validate_data(self):
        raise NotImplementedError('Subclass harus mengimplementasikan validate_data()')


class KunjunganManager(models.Manager): #encapsulation
    def antrean_dokter(self, dokter):
        return self.select_related(
            'pasien__user',
            'jadwal__dokter__user',
            'jadwal__poli'
        ).filter(
            jadwal__dokter=dokter
        )

    def antrean_rawat(self, dokter):
        return self.antrean_dokter(
            dokter
        ).filter(
            status__in=['diproses', 'rawat', 'resep']
        )

    def antrean_resep(self, dokter):
        return self.antrean_dokter(
            dokter
        ).filter(
            status__in=['rawat', 'resep']
        )

#polymorphism workflownya
class StatusWorkflow:
    def next_status(self):
        raise NotImplementedError


class DiprosesWorkflow(StatusWorkflow):
    def next_status(self):
        return 'rawat'


class RawatWorkflow(StatusWorkflow):
    def next_status(self):
        return 'resep'


class ResepWorkflow(StatusWorkflow):
    def next_status(self):
        return 'selesai'






class TindakanMedis(TimestampModel):
    kode_tindakan = models.CharField(max_length=10, unique=True, blank=True)
    nama_tindakan = models.CharField(max_length=100)
    tarif = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'tindakan_medis'

    def save(self, *args, **kwargs):
        if not self.kode_tindakan:
            self.kode_tindakan = (self.generate_kode_tindakan())

        super().save(*args, **kwargs)

    @classmethod
    def generate_kode_tindakan(cls):
        prefix = "TND-"
        last_instance = cls.objects.order_by('-id').first()

        if (last_instance and last_instance.kode_tindakan):
            try:
                last_number = int(last_instance.kode_tindakan.split('-')[1])
                new_number = last_number + 1
            except (IndexError, ValueError):
                new_number = 1

        else:
            new_number = 1

        return (f"{prefix}" f"{str(new_number).zfill(4)}")

    def __str__(self):
        return (
            f"{self.kode_tindakan}"
            f" - "
            f"{self.nama_tindakan}"
        )


class Kunjungan(TimestampModel):
    STATUS_DIPROSES = 'diproses'
    STATUS_RAWAT = 'rawat'
    STATUS_RESEP = 'resep'
    STATUS_SELESAI = 'selesai'

    pasien = models.ForeignKey('accounts.Pasien', on_delete=models.CASCADE)
    jadwal = models.ForeignKey('administrasi.JadwalPraktik', on_delete=models.CASCADE)
    tanggal_kunjungan = models.DateField()
    nomor_antrean = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default=STATUS_DIPROSES)
    objects = KunjunganManager()

    class Meta:
        db_table = 'kunjungan'

    @classmethod
    def generateNomorAntrean(cls, jadwal, tanggal_kunjungan):
        last_instance = cls.objects.filter(
            tanggal_kunjungan=tanggal_kunjungan,
            jadwal__poli=jadwal.poli
        ).order_by(
            'nomor_antrean'
        ).last()

        return (
            last_instance.nomor_antrean + 1
            if last_instance
            else 1
        )

    @classmethod
    def changeStatus(cls, kunjungan_id, status_baru):
        return cls.objects.filter(
            id=kunjungan_id
        ).update(
            status=status_baru
        )

    def get_workflow(self):
        workflows = {
            self.STATUS_DIPROSES:
                DiprosesWorkflow(),

            self.STATUS_RAWAT:
                RawatWorkflow(),

            self.STATUS_RESEP:
                ResepWorkflow(),
        }
        return workflows.get(self.status)

    def move_next_status(self):
        workflow = self.get_workflow()
        if workflow:
            self.status = (workflow.next_status())
            self.save()

        return self.status

    @property
    def kode_antrean(self):

        if (self.jadwal and self.jadwal.poli and self.nomor_antrean):
            kode_poli = (
                self.jadwal
                .poli
                .kode_poli
            )

            return (
                f"{kode_poli}"
                f"{str(self.nomor_antrean).zfill(3)}"
            )
        return "N/A"

    def __str__(self):
        return self.kode_antrean


class RekamMedis(BaseMedicalRecord):
    kunjungan = models.OneToOneField(Kunjungan, on_delete=models.CASCADE)
    keluhan = models.TextField()
    diagnosa = models.TextField()
    tekanan_darah = models.CharField(max_length=20)
    suhu_tubuh = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    class Meta:
        db_table = 'rekam_medis'

    def validate_data(self):
        if not self.keluhan:
            raise ValidationError('Keluhan wajib diisi.')

        if not self.diagnosa:
            raise ValidationError('Diagnosa wajib diisi.')

        if not self.tekanan_darah:
            raise ValidationError('Tekanan darah wajib diisi.')

        if self.suhu_tubuh is None:
            raise ValidationError('Suhu tubuh wajib diisi.')

        return True

    def update_pemeriksaan(self, keluhan, diagnosa, tekanan_darah, suhu_tubuh):
        self.keluhan = keluhan
        self.diagnosa = diagnosa
        self.tekanan_darah = tekanan_darah
        self.suhu_tubuh = suhu_tubuh
        self.validate_data()
        self.save()
        return self

    def __str__(self):
        return (
            f"RM - "
            f"{self.kunjungan.kode_antrean}"
        )


class TindakanRekamMedis(TimestampModel):
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE)
    tindakan_medis = models.ForeignKey('pelayanan.TindakanMedis', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tindakan_rekam_medis'

    def __str__(self):
        return (
            f"{self.rekam_medis.id}"
            f" - "
            f"{self.tindakan_medis.nama_tindakan}"
        )