from django.contrib import admin
from django.urls import path
from accounts import views as accounts_views
from master_data import views as master_data_views
from farmasi import views as farmasi_views

urlpatterns = [
    # Account Route
    path('generate-super-admin/', accounts_views.generate_superadmin, name='generate_super_admin'),

    path('admin/', admin.site.urls),
    path('', accounts_views.welcome_view,    name='welcome'),
    path('login/', accounts_views.login_view,    name='login'),
    path('register/', accounts_views.register_view, name='register'),
    path('logout/', accounts_views.logout_view,   name='logout'),
    path('dashboard/', accounts_views.dashboard_view, name='dashboard'),

    path('pasien/', accounts_views.pasien_index, name='pasien_index'),
    path('pasien/create', accounts_views.pasien_create, name='pasien_create'),
    path('pasien/<int:id>/edit', accounts_views.pasien_edit, name='pasien_edit'),
    path('pasien/<int:id>/delete', accounts_views.pasien_delete, name='pasien_delete'),

    path('dokter/', accounts_views.dokter_index, name='dokter_index'),
    path('dokter/create', accounts_views.dokter_create, name='dokter_create'),
    path('dokter/<int:id>/edit', accounts_views.dokter_edit, name='dokter_edit'),
    path('dokter/<int:id>/delete', accounts_views.dokter_delete, name='dokter_delete'),

    path('staff/', accounts_views.staff_index, name='staff_index'),
    path('staff/create', accounts_views.staff_create, name='staff_create'),
    path('staff/<int:id>/edit', accounts_views.staff_edit, name='staff_edit'),
    path('staff/<int:id>/delete', accounts_views.staff_delete, name='staff_delete'),

    # Master Data Route
    path('metode-pembayaran/', master_data_views.metode_pembayaran_index, name="metode_pembayaran_index"),
    path('metode-pembayaran/create', master_data_views.metode_pembayaran_create, name="metode_pembayaran_create"),
    path('metode-pembayaran/<int:id>/edit', master_data_views.metode_pembayaran_edit, name="metode_pembayaran_edit"),
    path('metode-pembayaran/<int:id>/delete', master_data_views.metode_pembayaran_delete, name="metode_pembarayan_delete"),

    path('poli/', master_data_views.poli_index, name="poli_index"),
    path('poli/create', master_data_views.poli_create, name="poli_create"),
    path('poli/<int:id>/edit', master_data_views.poli_edit, name="poli_edit"),
    path('poli/<int:id>/delete', master_data_views.poli_delete, name="poli_delete"),

    path('tindakan/', master_data_views.tindakan_medis_index, name="tindakan_medis_index"),
    path('tindakan/create', master_data_views.tindakan_medis_create, name="tindakan_medis_create"),
    path('tindakan/<int:id>/edit', master_data_views.tindakan_medis_edit, name="tindakan_medis_edit"),
    path('tindakan/<int:id>/delete', master_data_views.tindakan_medis_delete, name="tindakan_medis_delete"),

    path('jadwal/', master_data_views.jadwal_praktik_index, name="jadwal_praktik_index"),
    path('jadwal/create', master_data_views.jadwal_praktik_create, name="jadwal_praktik_create"),
    path('jadwal/<int:id>/edit', master_data_views.jadwal_praktik_edit, name="jadwal_praktik_edit"),
    path('jadwal/<int:id>/delete', master_data_views.jadwal_praktik_delete, name="jadwal_praktik_delete"),

    # Farmasi Route
    path('kategori-obat/', farmasi_views.kategori_obat_index, name="kategori_obat_index"),
    path('kategori-obat/create', farmasi_views.kategori_obat_create, name="kategori_obat_create"),
    path('kategori-obat/<int:id>/edit', farmasi_views.kategori_obat_edit, name="kategori_obat_edit"),
    path('kategori-obat/<int:id>/delete', farmasi_views.kategori_obat_delete, name="kategori_obat_delete"),
]