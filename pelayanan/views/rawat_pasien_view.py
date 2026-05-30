from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pelayanan.models import Kunjungan, RekamMedis, TindakanRekamMedis
from master_data.models import TindakanMedis

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

    if kunjungan_id:
        kunjungan = Kunjungan.objects.select_related(
            'pasien__user',
            'jadwal__dokter__user',
            'jadwal__poli'
        ).filter(
            id=kunjungan_id,
            jadwal__dokter = dokter
        ).first()

    else:
        kunjungan = Kunjungan.objects.select_related(
            'pasien__user',
            'jadwal__dokter__user',
            'jadwal__poli'
        ).filter(
            jadwal__dokter = dokter,
            status__in=['diproses', 'rawat']
        ).order_by('id').first()

    if kunjungan and kunjungan.status == 'diproses':
        kunjungan.status = 'rawat'
        kunjungan.save()


    if not kunjungan:
        context = {
            'page_title': 'Rawat Pasien',
            'kunjungan': None,
            'tindakan_list': [],
            'riwayat_rekam_medis': [],
        }

        return render(
            request,
            'pages/pelayanan/rawat_pasien/index.html',
            context
        )

    tindakan_list = TindakanMedis.objects.all()

    rekam_medis = RekamMedis.objects.filter(
        kunjungan=kunjungan
    ).first()

    selected_tindakan_ids = []

    if rekam_medis:
        selected_tindakan_ids = TindakanRekamMedis.objects.filter(
            rekam_medis=rekam_medis
        ).values_list(
            'tindakan_medis_id',
            flat=True
        )

    if request.method == 'POST':
        keluhan = request.POST.get('keluhan', '').strip()
        diagnosa = request.POST.get('diagnosa', '').strip()
        tekanan_darah = request.POST.get('tekanan_darah', '').strip()
        suhu_tubuh = request.POST.get('suhu_tubuh', '').strip()
        tindakan_ids = request.POST.getlist('tindakan_ids')

        if not keluhan:
            messages.error(
                request,
                'Keluhan pasien wajib diisi.'
            )

            return redirect(
                'rawat_pasien_detail',
                kunjungan_id=kunjungan.id
            )

        if not diagnosa:
            messages.error(
                request,
                'Diagnosa wajib diisi.'
            )

            return redirect(
                'rawat_pasien_detail',
                kunjungan_id=kunjungan.id
            )

        if not tekanan_darah:
            messages.error(
                request,
                'Tekanan darah wajib diisi.'
            )

            return redirect(
                'rawat_pasien_detail',
                kunjungan_id=kunjungan.id
            )

        if not suhu_tubuh:
            messages.error(
                request,
                'Suhu tubuh wajib diisi.'
            )

            return redirect(
                'rawat_pasien_detail',
                kunjungan_id=kunjungan.id
            )

        if len(tindakan_ids) < 1:
            messages.error(
                request,
                'Minimal pilih 1 tindakan medis.'
            )

            return redirect(
                'rawat_pasien_detail',
                kunjungan_id=kunjungan.id
            )

        rekam_medis, created = RekamMedis.objects.get_or_create(
            kunjungan=kunjungan,
            defaults={
                'keluhan': keluhan,
                'diagnosa': diagnosa,
                'tekanan_darah': tekanan_darah,
                'suhu_tubuh': suhu_tubuh,
            }
        )

        if not created:
            rekam_medis.keluhan = keluhan
            rekam_medis.diagnosa = diagnosa
            rekam_medis.tekanan_darah = tekanan_darah
            rekam_medis.suhu_tubuh = suhu_tubuh
            rekam_medis.save()

        TindakanRekamMedis.objects.filter(
            rekam_medis=rekam_medis
        ).delete()

        for tindakan_id in tindakan_ids:
            tindakan = TindakanMedis.objects.get(
                id=tindakan_id
            )

            TindakanRekamMedis.objects.create(
                rekam_medis=rekam_medis,
                tindakan_medis=tindakan
            )


        messages.success(
            request,
            'Data pemeriksaan berhasil disimpan.'
        )

        kunjungan.status = 'resep'
        kunjungan.save()

        return redirect(
            'resep_obat_detail',
            kunjungan_id=kunjungan.id
        )

    riwayat_rekam_medis = RekamMedis.objects.filter(
        kunjungan__pasien=kunjungan.pasien
    ).exclude(
        kunjungan=kunjungan
    ).order_by('-id')

    context = {
        'page_title': 'Rawat Pasien',
        'kunjungan': kunjungan,
        'tindakan_list': tindakan_list,
        'riwayat_rekam_medis': riwayat_rekam_medis,
        'rekam_medis': rekam_medis,
        'selected_tindakan_ids': selected_tindakan_ids,
    }

    return render(
        request,
        'pages/pelayanan/rawat_pasien/index.html',
        context
    )

