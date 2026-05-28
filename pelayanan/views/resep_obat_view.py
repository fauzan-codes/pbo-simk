from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pelayanan.models import Kunjungan, RekamMedis
from farmasi.models import Obat, Resep, DetailResep


@login_required
def resep_obat_index(request, kunjungan_id=None):
    # if not hasattr(request.user, 'dokter'):
    #     messages.error(
    #         request,
    #         'Akun ini bukan akun dokter.'
    #     )
    #     return redirect('dashboard')
    # dokter = request.user.dokter

    if kunjungan_id:
        kunjungan = Kunjungan.objects.select_related(
            'pasien__user',
            'jadwal__dokter__user',
            'jadwal__poli'
        ).filter(
            id=kunjungan_id,
            # jadwal__dokter = dokter
        ).first()

    else:
        kunjungan = Kunjungan.objects.select_related(
            'pasien__user',
            'jadwal__dokter__user',
            'jadwal__poli'
        ).filter(
            # jadwal__dokter = dokter,
            status__in=['rawat', 'resep']
        ).order_by('id').first()

    # if (kunjungan and kunjungan.dokter_penanggung_jawab and kunjungan.dokter_penanggung_jawab != dokter):
    #     messages.error(
    #         request,
    #         'Pasien sedang ditangani dokter lain.'
    #     )

    #     return redirect(
    #         'resep_obat_index'
    #     )

    if not kunjungan:
        context = {
            'page_title': 'Resep Obat',
            'kunjungan': None,
            'rekam_medis': None,
            'obat_list': [],
            'detail_resep': [],
            'is_rekam_medis_exist': False,
        }

        return render(
            request,
            'pages/pelayanan/resep_obat/index.html',
            context
        )

    rekam_medis = RekamMedis.objects.filter(
        kunjungan=kunjungan
    ).first()

    is_rekam_medis_exist = rekam_medis is not None

    obat_list = Obat.objects.select_related(
        'kategori'
    ).all().order_by('id')

    resep = None
    detail_resep = []

    if rekam_medis:
        resep, created = Resep.objects.get_or_create(
            rekam_medis=rekam_medis,
            defaults={
                'status': 'diproses'
            }
        )

        detail_resep = DetailResep.objects.filter(
            resep=resep
        ).select_related(
            'obat',
            'obat__kategori'
        )

    if request.method == 'POST':
        if not rekam_medis:
            messages.error(
                request,
                'Dokter harus menyelesaikan pemeriksaan terlebih dahulu.'
            )

            return redirect(
                'rawat_pasien_detail',
                kunjungan_id=kunjungan.id
            )

        obat_ids = request.POST.getlist('obat_ids')
        selected_items = []

        for obat_id in obat_ids:
            selected_items.append({
                'obat_id': obat_id,
                'jumlah': 1
            })

        if len(selected_items) < 1:
            messages.error(
                request,
                'Minimal pilih 1 obat.'
            )

            return redirect(
                'resep_obat_detail',
                kunjungan_id=kunjungan.id
            )

        DetailResep.objects.filter(
            resep=resep
        ).delete()

        for item in selected_items:
            obat = Obat.objects.get(
                id=item['obat_id']
            )

            DetailResep.objects.create(
                resep=resep,
                obat=obat,
                jumlah_diminta=item['jumlah'],
                dosis_aturan='-',
                subtotal_harga=(
                    int(item['jumlah']) * obat.harga_jual
                )
            )

        kunjungan.status = 'selesai'
        kunjungan.save()

        messages.success(
            request,
            'Resep obat berhasil disimpan.'
        )

        return redirect(
            'resep_obat_index'
        )

    context = {
        'page_title': 'Resep Obat',
        'kunjungan': kunjungan,
        'rekam_medis': rekam_medis,
        'obat_list': obat_list,
        'detail_resep': detail_resep,
        'is_rekam_medis_exist': is_rekam_medis_exist,
    }

    return render(
        request,
        'pages/pelayanan/resep_obat/index.html',
        context
    )