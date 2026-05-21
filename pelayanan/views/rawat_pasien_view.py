# pelayanan/views/rawat_pasien_view.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pelayanan.models import (
    Kunjungan,
    RekamMedis,
    TindakanRekamMedis
)

from master_data.models import TindakanMedis


@login_required
def rawat_pasien_detail(request, kunjungan_id=None):

    if kunjungan_id:

        kunjungan = Kunjungan.objects.filter(
            id=kunjungan_id
        ).first()

    else:

        kunjungan = Kunjungan.objects.first()

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

    if request.method == 'POST':

        keluhan = request.POST.get('keluhan')
        diagnosa = request.POST.get('diagnosa')
        tekanan_darah = request.POST.get('tekanan_darah')
        suhu_tubuh = request.POST.get('suhu_tubuh')

        tindakan_ids = request.POST.getlist('tindakan_ids')

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

        kunjungan.status = 'selesai'
        kunjungan.save()

        messages.success(
            request,
            'Data rekam medis berhasil disimpan.'
        )

        return redirect(
            'rawat_pasien_detail',
            kunjungan_id=kunjungan.id
        )

    riwayat_rekam_medis = RekamMedis.objects.filter(
        kunjungan__pasien=kunjungan.pasien
    ).order_by('-id')

    context = {
        'page_title': 'Rawat Pasien',
        'kunjungan': kunjungan,
        'tindakan_list': tindakan_list,
        'riwayat_rekam_medis': riwayat_rekam_medis,
    }

    return render(
        request,
        'pages/pelayanan/rawat_pasien/index.html',
        context
    )
