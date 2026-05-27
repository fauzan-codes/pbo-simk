from django.urls import path
from .views import *

urlpatterns = [

    path(
        'rawat-pasien/',
        rawat_pasien_detail,
        name='rawat_pasien_index'
    ),

    path(
        'rawat-pasien/<int:kunjungan_id>/',
        rawat_pasien_detail,
        name='rawat_pasien_detail'
    ),

    path(
        'resep-obat/',
        resep_obat_index,
        name='resep_obat_index'
    ),

    path(
        'resep-obat/<int:kunjungan_id>/',
        resep_obat_index,
        name='resep_obat_detail'
    ),
    
]