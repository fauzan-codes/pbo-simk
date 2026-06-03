from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pelayanan.models import Kunjungan, RekamMedis, TindakanMedis, TindakanRekamMedis


class RawatPasienRepository:
    @staticmethod
    def get_kunjungan(dokter, kunjungan_id=None):
        if kunjungan_id:
            return Kunjungan.objects.select_related(
                'pasien__user',
                'jadwal__dokter__user',
                'jadwal__poli'
            ).filter(
                id=kunjungan_id,
                jadwal__dokter=dokter
            ).first()

        return (
            Kunjungan.objects
            .antrean_rawat(dokter)
            .order_by('id')
            .first()
        )

    @staticmethod
    def get_tindakan_list():
        return TindakanMedis.objects.order_by('nama_tindakan')

    @staticmethod
    def get_rekam_medis(kunjungan):
        return RekamMedis.objects.filter(kunjungan=kunjungan).first()

    @staticmethod
    def get_selected_tindakan_ids(rekam_medis):
        if not rekam_medis:
            return []

        return list(
            TindakanRekamMedis.objects.filter(
                rekam_medis=rekam_medis
            ).values_list(
                'tindakan_medis_id', 
                flat=True
            )
        )

    @staticmethod
    def get_riwayat_rekam_medis(pasien, current_kunjungan):
        return RekamMedis.objects.filter(
            kunjungan__pasien=pasien
        ).exclude(
            kunjungan=current_kunjungan
        ).order_by('-id')



class RawatPasienService:
    def __init__(self, kunjungan):
        self.kunjungan = kunjungan

    @staticmethod
    def validate_input(keluhan, diagnosa, tekanan_darah, suhu_tubuh, tindakan_ids):
        if not keluhan:
            raise ValueError('Keluhan pasien wajib diisi.')

        if not diagnosa:
            raise ValueError('Diagnosa wajib diisi.')

        if not tekanan_darah:
            raise ValueError('Tekanan darah wajib diisi.')

        if not suhu_tubuh:
            raise ValueError('Suhu tubuh wajib diisi.')

        if len(tindakan_ids) < 1:
            raise ValueError('Minimal pilih 1 tindakan medis.')

    def save_rekam_medis(self, keluhan, diagnosa, tekanan_darah, suhu_tubuh):
        rekam_medis, created = (
            RekamMedis.objects.get_or_create(
                kunjungan=self.kunjungan,
                defaults={
                    'keluhan': keluhan,
                    'diagnosa': diagnosa,
                    'tekanan_darah': tekanan_darah,
                    'suhu_tubuh': suhu_tubuh
                }
            )
        )

        if not created:
            rekam_medis.update_pemeriksaan(keluhan=keluhan, diagnosa=diagnosa, tekanan_darah=tekanan_darah, suhu_tubuh=suhu_tubuh)

        return rekam_medis

    @staticmethod
    def save_tindakan(rekam_medis, tindakan_ids):
        TindakanRekamMedis.objects.filter(rekam_medis=rekam_medis).delete()
        tindakan_list = (TindakanMedis.objects.filter(id__in=tindakan_ids))
        tindakan_objects = []

        for tindakan in tindakan_list:
            tindakan_objects.append(TindakanRekamMedis(rekam_medis=rekam_medis, tindakan_medis=tindakan))

        TindakanRekamMedis.objects.bulk_create(tindakan_objects)

    def finalisasi(self, keluhan, diagnosa, tekanan_darah, suhu_tubuh, tindakan_ids):
        self.validate_input(keluhan, diagnosa, tekanan_darah, suhu_tubuh, tindakan_ids)
        rekam_medis = (self.save_rekam_medis(keluhan, diagnosa, tekanan_darah, suhu_tubuh))
        self.save_tindakan(rekam_medis, tindakan_ids)

        #polymorphism
        self.kunjungan.move_next_status()
        return rekam_medis



@login_required
def rawat_pasien_detail(request, kunjungan_id=None):
    if request.user.role != 'dokter':
        messages.error(
            request,
            'Akun ini bukan akun dokter.'
        )
        return redirect('dashboard')

    dokter = getattr(request.user, 'dokter_profile', None)

    if not dokter:
        messages.error(
            request,
            'Profile dokter tidak ditemukan.'
        )
        return redirect('dashboard')

    kunjungan = (
        RawatPasienRepository
        .get_kunjungan(dokter, kunjungan_id)
    )

    if (kunjungan and kunjungan.status == 'diproses'):
        kunjungan.move_next_status()

    if not kunjungan:
        return render(
            request,
            'pages/pelayanan/rawat_pasien/index.html',
            {
                'page_title':
                    'Rawat Pasien',

                'kunjungan':
                    None,

                'tindakan_list':
                    [],

                'riwayat_rekam_medis':
                    []
            }
        )

    tindakan_list = (
        RawatPasienRepository
        .get_tindakan_list()
    )

    rekam_medis = (
        RawatPasienRepository
        .get_rekam_medis(kunjungan)
    )

    selected_tindakan_ids = (
        RawatPasienRepository
        .get_selected_tindakan_ids(rekam_medis)
    )

    if request.method == 'POST':
        try:
            service = (RawatPasienService(kunjungan))
            service.finalisasi(
                keluhan=request.POST.get('keluhan', '').strip(),
                diagnosa=request.POST.get('diagnosa', '').strip(),
                tekanan_darah=request.POST.get('tekanan_darah', '').strip(),
                suhu_tubuh=request.POST.get('suhu_tubuh', '').strip(),
                tindakan_ids=request.POST.getlist('tindakan_ids')
            )

            messages.success(
                request,
                (
                    'Data pemeriksaan '
                    'berhasil disimpan.'
                )
            )

            return redirect(
                'resep_obat_detail',
                kunjungan_id=kunjungan.id
            )

        except ValueError as e:
            messages.error(request, str(e))

            return redirect(
                'rawat_pasien_detail',
                kunjungan_id=kunjungan.id
            )

    riwayat_rekam_medis = (
        RawatPasienRepository
        .get_riwayat_rekam_medis(kunjungan.pasien, kunjungan)
    )

    context = {
        'page_title':
            'Rawat Pasien',

        'kunjungan':
            kunjungan,

        'tindakan_list':
            tindakan_list,

        'riwayat_rekam_medis':
            riwayat_rekam_medis,

        'rekam_medis':
            rekam_medis,

        'selected_tindakan_ids':
            selected_tindakan_ids
    }

    return render(
        request,
        'pages/pelayanan/rawat_pasien/index.html',
        context
    )