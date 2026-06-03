from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pelayanan.models import Kunjungan, RekamMedis
from farmasi.models import Obat, Resep, DetailResep



class ResepRepository:
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
            .antrean_resep(dokter)
            .order_by('id')
            .first()
        )

    @staticmethod
    def get_rekam_medis(kunjungan):
        return RekamMedis.objects.filter(kunjungan=kunjungan).first()

    @staticmethod
    def get_obat_list():
        return (
            Obat.objects
            .select_related('kategori')
            .order_by('id')
        )

    @staticmethod
    def get_resep(rekam_medis):
        return Resep.objects.get_or_create(
            rekam_medis=rekam_medis,
            defaults={
                'status': 'diproses'
            }
        )

    @staticmethod
    def get_detail_resep(resep):
        return DetailResep.objects.filter(
            resep=resep
        ).select_related(
            'obat',
            'obat__kategori'
        )


class ResepService:
    def __init__(self, resep):
        self.resep = resep

    def save_resep(self, selected_items):
        DetailResep.objects.filter(resep=self.resep).delete()

        for item in selected_items:
            obat = Obat.objects.get(id=item['obat_id'])

            DetailResep.objects.create(
                resep=self.resep,
                obat=obat,
                jumlah_diminta=item['jumlah'],
                dosis_aturan=item['dosis_aturan'],
                subtotal_harga=(item['jumlah']*obat.harga_jual)
            )

    @staticmethod
    def extract_post_data(request):
        obat_ids = request.POST.getlist('obat_ids')
        selected_items = []

        for obat_id in obat_ids:
            dosis_aturan = (
                request.POST.get(f'dosis_aturan_{obat_id}', '-')
            )

            selected_items.append({
                'obat_id': obat_id,
                'jumlah': 1,
                'dosis_aturan':
                    dosis_aturan
            })

        return selected_items



@login_required
def resep_obat_index(request, kunjungan_id=None):

    if request.user.role != 'dokter':
        messages.error(request, 'Akun ini bukan akun dokter.')
        return redirect('dashboard')

    dokter = getattr(request.user, 'dokter_profile', None)

    if not dokter:
        messages.error(request, 'Profile dokter tidak ditemukan.')
        return redirect('dashboard')

    kunjungan = (
        ResepRepository
        .get_kunjungan(dokter, kunjungan_id)
    )

    if not kunjungan:
        return render(
            request,
            'pages/pelayanan/resep_obat/index.html',
            {
                'page_title':
                    'Resep Obat',

                'kunjungan':
                    None,

                'rekam_medis':
                    None,

                'obat_list':
                    [],

                'detail_resep':
                    [],

                'is_rekam_medis_exist':
                    False,
            }
        )

    rekam_medis = (
        ResepRepository
        .get_rekam_medis(kunjungan)
    )

    is_rekam_medis_exist = (rekam_medis is not None)
    obat_list = (ResepRepository.get_obat_list())

    resep = None
    detail_resep = []

    if rekam_medis:
        resep, created = (
            ResepRepository
            .get_resep(rekam_medis)
        )

        detail_resep = (
            ResepRepository
            .get_detail_resep(resep)
        )

    if request.method == 'POST':
        if not rekam_medis:
            messages.error(
                request,
                (
                    'Dokter harus '
                    'menyelesaikan '
                    'pemeriksaan '
                    'terlebih dahulu.'
                )
            )

            return redirect('rawat_pasien_detail', kunjungan_id=kunjungan.id)

        selected_items = (
            ResepService
            .extract_post_data(request)
        )

        service = ResepService(resep)
        service.save_resep(selected_items)
        kunjungan.move_next_status()

        messages.success(request, 'Resep obat berhasil disimpan.')
        return redirect('resep_obat_index')

    context = {
        'page_title':
            'Resep Obat',

        'kunjungan':
            kunjungan,

        'rekam_medis':
            rekam_medis,

        'obat_list':
            obat_list,

        'detail_resep':
            detail_resep,

        'is_rekam_medis_exist':
            is_rekam_medis_exist,
    }

    return render(
        request,
        'pages/pelayanan/resep_obat/index.html',
        context
    )