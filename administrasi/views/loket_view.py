from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Loket
from django.urls import reverse

import json
import os
from django.http import JsonResponse
import paho.mqtt.publish as publish
from django.views.decorators.csrf import csrf_exempt

@login_required
def loket_index(request):
    loket_list = Loket.objects.all()
    context = {
        'loket_list': loket_list,
        'breadcrumbs': [
            {'name': 'Manajemen Loket', 'url': reverse('loket_index')},
        ],
        'page_title': 'Manajemen Loket'
    }
    return render(request, 'pages/administrasi/loket/index.html', context)

@login_required
def loket_create(request):
    if request.method == "POST":
        try:
            nama_loket = request.POST.get('nama_loket')

            Loket.objects.create(
                nama_loket = nama_loket,
            )

            messages.success(request, f'Data {nama_loket} berhasil ditambahkan.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return redirect('loket_index')

@login_required
def loket_edit(request, id):
    try:
        loket = Loket.objects.get(id=id)
    except loket.DoesNotExist:
        messages.error(request, "Loket tidak ditemukan.")
        return redirect('loket_index')
    
    if request.method == "POST":
        try:
            nama_loket = request.POST.get('nama_loket')
            loket.nama_loket =  nama_loket
            loket.save()

            messages.success(request, f'Data {nama_loket} berhasil diupdate.')
            return redirect('loket_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    context = {
        'loket': loket,
        'breadcrumbs': [
            {'name': 'Manajemen Loket', 'url': reverse('loket_index')},
            {'name': 'Edit Loket', 'url': None},
        ],
        'page_title': 'Edit Loket'
    }
    return render(request, 'pages/administrasi/loket/edit.html', context)

@login_required
def loket_delete(request, id):
    try:
        loket = Loket.objects.get(id=id)
        loket.delete()
        messages.success(request, 'Data loket berhasil dihapus.')
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return redirect('loket_index')



@csrf_exempt
def api_set_loket(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        loket_id = data.get('loket_id')
        action = data.get('action')

        try:
            loket = Loket.objects.get(id=loket_id)
            
            if action == 'start':
                loket.staff = request.user.staff_profile
                
                request.session['active_loket_id'] = str(loket_id)
                
            elif action == 'stop':
                loket.staff = None
                loket.kunjungan = None 
                
                if 'active_loket_id' in request.session:
                    del request.session['active_loket_id']

            loket.save()

            mqtt_host = os.environ.get('MQTT_HOST', 'localhost')
            mqtt_port = int(os.environ.get('MQTT_PORT', 1883))
            
            publish.single(
                topic="simk/antrean/refresh", 
                payload=json.dumps({"action": "update_status_loket"}), 
                hostname=mqtt_host, 
                port=mqtt_port
            )

            return JsonResponse({'status': 'success'})
        except Loket.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Loket tidak ditemukan'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'invalid method'}, status=405)