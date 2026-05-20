import json
import os
import paho.mqtt.publish as publish
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pelayanan.models import Kunjungan
from administrasi.models import Loket
from master_data.models import JadwalPraktik

def antrean_index(request):
    mqtt_url = os.environ.get('MQTT_WEBSOCKET_URL', 'ws://localhost:9001/mqtt')
    context = {
        'page_title': 'Daftar Antrian',
        'mqtt_url': mqtt_url
    }
    return render(request, 'pages/administrasi/antrean/index.html', context)

def antrean_loket_view(request):
    loket_list = Loket.objects.all()
    return render(request, 'antrean/dashboard_loket.html', {'loket_list': loket_list})

def api_get_antrean(request):
    kunjungan_aktif_ids = Loket.objects.filter(
        kunjungan__isnull=False
    ).values_list('kunjungan_id', flat=True)

    antrean_tersedia = Kunjungan.objects.filter(
        status='menunggu'
    ).exclude(
        id__in=kunjungan_aktif_ids
    ).select_related('jadwal', 'jadwal__poli', 'pasien').order_by('tanggal_kunjungan', 'nomor_antrean')

    data_antrean = []
    for k in antrean_tersedia:
        data_antrean.append({
            'id': k.id,
            'kode_antrean': k.kode_antrean,
            'nomor_antrean': k.nomor_antrean,
            'poli': k.jadwal.poli.nama_poli if k.jadwal and k.jadwal.poli else 'N/A',
            'pasien': k.pasien.user.full_name if k.pasien and k.pasien.user else 'N/A',
            'tanggal': k.tanggal_kunjungan.strftime('%d-%m-%Y')
        })

    data_loket = []
    lokets = Loket.objects.select_related('kunjungan', 'staff', 'staff__user').all()
    for l in lokets:
        data_loket.append({
            'id': l.id,
            'nama_loket': l.nama_loket,
            'kunjungan_id': l.kunjungan.id if l.kunjungan else None,
            'pasien_dipanggil': l.kunjungan.kode_antrean if l.kunjungan else '-',
            'staff': l.staff.user.full_name if l.staff and l.staff.user else '-'
        })

    return JsonResponse({
        'antrean': data_antrean,
        'loket': data_loket
    })

@csrf_exempt
def api_panggil_pasien(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        kunjungan_id = data.get('kunjungan_id')
        loket_id = data.get('loket_id')

        try:
            Kunjungan.changeStatus(kunjungan_id, 'diproses')

            loket = Loket.objects.get(id=loket_id)
            loket.kunjungan_id = kunjungan_id
            loket.save()

            mqtt_host = os.environ.get('MQTT_HOST', 'localhost')
            mqtt_port = int(os.environ.get('MQTT_PORT', 1883)) 
            
            topic = "simk/antrean/refresh"
            
            payload = json.dumps({
                "action": "fetch_ulang",
                "loket_id": loket_id,
                "kunjungan_id": kunjungan_id
            })

            publish.single(
                topic=topic, 
                payload=payload, 
                hostname=mqtt_host, 
                port=mqtt_port
            )
            
            return JsonResponse({'status': 'success', 'message': 'Pasien berhasil dipanggil'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'invalid method'}, status=405)

def monitor_index(request):
    mqtt_url = os.environ.get('MQTT_WEBSOCKET_URL', 'ws://localhost:9001/mqtt')
    
    context = {
        'page_title': 'Monitor Antrean',
        'mqtt_url': mqtt_url
    }
    
    return render(request, 'pages/administrasi/monitor/index.html', context)