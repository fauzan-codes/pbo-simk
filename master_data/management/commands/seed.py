from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from accounts.models import User, Dokter, Staff, Pasien
from master_data.models import Poli, JadwalPraktik, TindakanMedis, MetodePembayaran
from pelayanan.models import Kunjungan, RekamMedis, TindakanRekamMedis
from farmasi.models import KategoriObat, Obat, Resep, DetailResep
from keuangan.models import Tagihan
from administrasi.models import Loket


class Command(BaseCommand):
    help = 'Seed database dengan data testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus semua data sebelum seed',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_database()

        self.stdout.write(self.style.SUCCESS('🌱 Mulai seeding database...'))
        
        # Seed data
        self.seed_users()
        self.seed_poli()
        self.seed_tindakan_medis()
        self.seed_metode_pembayaran()
        self.seed_jadwal_praktik()
        self.seed_kategori_obat()
        self.seed_obat()
        self.seed_kunjungan()
        self.seed_rekam_medis()
        self.seed_resep()
        self.seed_tagihan()
        self.seed_loket()

        self.stdout.write(self.style.SUCCESS('✅ Database seeding selesai!'))

    def clear_database(self):
        self.stdout.write(self.style.WARNING('🗑️ Menghapus data lama...'))
        models = [
            Loket, Tagihan, DetailResep, Resep, Obat, KategoriObat,
            TindakanRekamMedis, RekamMedis, Kunjungan, JadwalPraktik,
            MetodePembayaran, TindakanMedis, Poli, Dokter, Staff, Pasien, User
        ]
        for model in models:
            model.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Data lama berhasil dihapus'))

    def seed_users(self):
        self.stdout.write('📝 Membuat User...')
        
        # Admin
        admin = User.objects.create_user(
            full_name='Superadmin',
            username='superadmin',
            email='admin@simk.com',
            password='password',
            role="admin"
        )
        
        # Dokter
        dokter_user = User.objects.create_user(
            full_name='Dr. Budi Santoso',
            username='dokter_budi',
            email='budi@simk.com',
            password='password',
            role='dokter'
        )
        
        Dokter.objects.create(
            user=dokter_user,
            spesialisasi='Umum',
            nomor_sip='12345/2020',
            tarif_jasa=Decimal('150000.00'),
            no_hp='081234567890',
            alamat='Jl. Merdeka No. 10'
        )
        
        # Dokter 2
        dokter_user2 = User.objects.create_user(
            full_name='Dr. Siti Nurhaliza',
            username='dokter_siti',
            email='siti@simk.com',
            password='dokter123',
            role='dokter'
        )
        
        Dokter.objects.create(
            user=dokter_user2,
            spesialisasi='Gigi',
            nomor_sip='54321/2020',
            tarif_jasa=Decimal('200000.00'),
            no_hp='081234567891',
            alamat='Jl. Sudirman No. 20'
        )
        
        # Staff - Administrasi
        staff_user = User.objects.create_user(
            full_name='Rina Wijaya',
            username='staff_rina',
            email='rina@simk.com',
            password='password',
            role='staff',
        )
        
        Staff.objects.create(
            user=staff_user,
            jabatan='Administrasi',
            shift_kerja='Pagi',
            no_hp='082345678901',
            alamat='Jl. Gatot Subroto No. 5'
        )
        
        # Staff - Kasir
        staff_user2 = User.objects.create_user(
            full_name='Hendra Gunawan',
            username='staff_hendra',
            email='hendra@simk.com',
            password='password',
            role='staff',
        )
        
        Staff.objects.create(
            user=staff_user2,
            jabatan='Kasir',
            shift_kerja='Siang',
            no_hp='082345678902',
            alamat='Jl. Ahmad Yani No. 15'
        )
        
        # Staff - Apoteker
        staff_user3 = User.objects.create_user(
            full_name='Diana Putri',
            username='staff_diana',
            email='diana@simk.com',
            password='password',
            role='staff',
        )
        
        Staff.objects.create(
            user=staff_user3,
            jabatan='Apoteker',
            shift_kerja='Pagi',
            no_hp='082345678903',
            alamat='Jl. Diponegoro No. 25'
        )
        
        # Pasien
        pasien_user = User.objects.create_user(
            full_name='Bambang Sutrisno',
            username='pasien_bambang',
            email='bambang@simk.com',
            password='password',
            role='pasien'
        )
        
        Pasien.objects.create(
            user=pasien_user,
            nik='3213140589900001',
            tanggal_lahir=datetime(1990, 9, 5).date(),
            jenis_kelamin='L',
            alamat='Jl. Kemerdekaan No. 100',
            no_hp='083456789012'
        )
        
        # Pasien 2
        pasien_user2 = User.objects.create_user(
            full_name='Siti Nurhaliza',
            username='pasien_siti',
            email='sitiharsha@simk.com',
            password='pasien123',
            role='pasien'
        )
        
        Pasien.objects.create(
            user=pasien_user2,
            nik='3213140592850002',
            tanggal_lahir=datetime(1985, 3, 12).date(),
            jenis_kelamin='P',
            alamat='Jl. Merdeka No. 50',
            no_hp='083456789013'
        )
        
        self.stdout.write(self.style.SUCCESS('✓ User berhasil dibuat'))

    def seed_poli(self):
        self.stdout.write('🏥 Membuat Poli...')
        
        poli_data = [
            ('U', 'Poli Umum'),
            ('G', 'Poli Gigi'),
            ('K', 'Poli KIA'),
            ('T', 'Poli TB'),
        ]
        
        for kode, nama in poli_data:
            Poli.objects.create(kode_poli=kode, nama_poli=nama)
        
        self.stdout.write(self.style.SUCCESS('✓ Poli berhasil dibuat'))

    def seed_tindakan_medis(self):
        self.stdout.write('💉 Membuat Tindakan Medis...')
        
        tindakan_data = [
            ('Pemeriksaan Umum', Decimal('50000.00')),
            ('Injeksi', Decimal('75000.00')),
            ('Perawatan Gigi', Decimal('150000.00')),
            ('Pembersihan Gigi', Decimal('100000.00')),
            ('Pemeriksaan TB', Decimal('200000.00')),
        ]
        
        for nama, tarif in tindakan_data:
            TindakanMedis.objects.create(nama_tindakan=nama, tarif=tarif)
        
        self.stdout.write(self.style.SUCCESS('✓ Tindakan Medis berhasil dibuat'))

    def seed_metode_pembayaran(self):
        self.stdout.write('💳 Membuat Metode Pembayaran...')
        
        metode_data = ['Tunai', 'Debit', 'Kredit', 'Transfer']
        
        for metode in metode_data:
            MetodePembayaran.objects.create(nama_metode=metode)
        
        self.stdout.write(self.style.SUCCESS('✓ Metode Pembayaran berhasil dibuat'))

    def seed_jadwal_praktik(self):
        self.stdout.write('📅 Membuat Jadwal Praktik...')
        
        dokter_list = Dokter.objects.all()
        poli_list = Poli.objects.all()
        
        hari_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
        
        for i, dokter in enumerate(dokter_list):
            poli = poli_list[i % len(poli_list)]
            for j, hari in enumerate(hari_list):
                JadwalPraktik.objects.create(
                    dokter=dokter,
                    poli=poli,
                    hari=hari,
                    jam_mulai=timezone.now().replace(hour=8, minute=0).time(),
                    jam_selesai=timezone.now().replace(hour=12, minute=0).time()
                )
        
        self.stdout.write(self.style.SUCCESS('✓ Jadwal Praktik berhasil dibuat'))

    def seed_kategori_obat(self):
        self.stdout.write('💊 Membuat Kategori Obat...')
        
        kategori_data = ['Analgesik', 'Antibiotik', 'Antiinflamasi', 'Vitamin']
        
        for nama in kategori_data:
            KategoriObat.objects.create(nama_kategori=nama)
        
        self.stdout.write(self.style.SUCCESS('✓ Kategori Obat berhasil dibuat'))

    def seed_obat(self):
        self.stdout.write('💊 Membuat Obat...')
        
        kategori_list = KategoriObat.objects.all()
        
        obat_data = [
            ('Paracetamol', 'OBT-001', 0, 'Tablet', 100, Decimal('2500.00')),
            ('Amoxicillin', 'OBT-002', 1, 'Kaplet', 50, Decimal('5000.00')),
            ('Ibuprofen', 'OBT-003', 2, 'Tablet', 75, Decimal('3500.00')),
            ('Vitamin C', 'OBT-004', 3, 'Tablet', 200, Decimal('1500.00')),
            ('Metronidazole', 'OBT-005', 1, 'Tablet', 60, Decimal('4000.00')),
        ]
        
        for nama, kode, kategori_idx, satuan, stok, harga in obat_data:
            Obat.objects.create(
                nama_obat=nama,
                kode_obat=kode,
                kategori=kategori_list[kategori_idx],
                satuan=satuan,
                stok=stok,
                harga_jual=harga
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Obat berhasil dibuat'))

    def seed_kunjungan(self):
        self.stdout.write('👥 Membuat Kunjungan...')
        
        pasien_list = Pasien.objects.filter(user__isnull=False)
        jadwal_list = JadwalPraktik.objects.all()
        
        if pasien_list.exists() and jadwal_list.exists():
            for i, pasien in enumerate(pasien_list):
                jadwal = jadwal_list[i % len(jadwal_list)]
                tanggal = timezone.now().date() + timedelta(days=i)
                
                kunjungan = Kunjungan.objects.create(
                    pasien=pasien,
                    jadwal=jadwal,
                    tanggal_kunjungan=tanggal,
                    nomor_antrean=i + 1,
                    status='diproses'
                )
        
        self.stdout.write(self.style.SUCCESS('✓ Kunjungan berhasil dibuat'))

    def seed_rekam_medis(self):
        self.stdout.write('📋 Membuat Rekam Medis...')
        
        kunjungan_list = Kunjungan.objects.all()
        tindakan_list = TindakanMedis.objects.all()
        
        for kunjungan in kunjungan_list:
            rekam_medis = RekamMedis.objects.create(
                kunjungan=kunjungan,
                keluhan='Demam dan batuk',
                diagnosa='Influenza',
                tekanan_darah='120/80',
                suhu_tubuh=Decimal('37.5')
            )
            
            # Tambah 2 tindakan ke rekam medis
            for tindakan in tindakan_list[:2]:
                TindakanRekamMedis.objects.create(
                    rekam_medis=rekam_medis,
                    tindakan_medis=tindakan
                )
        
        self.stdout.write(self.style.SUCCESS('✓ Rekam Medis berhasil dibuat'))

    def seed_resep(self):
        self.stdout.write('💊 Membuat Resep...')
        
        rekam_medis_list = RekamMedis.objects.all()
        staff_apoteker = Staff.objects.filter(jabatan='Apoteker').first()
        obat_list = Obat.objects.all()
        
        for rekam_medis in rekam_medis_list:
            resep = Resep.objects.create(
                rekam_medis=rekam_medis,
                apoteker=staff_apoteker,
                status='diproses'
            )
            
            # Tambah detail resep
            for obat in obat_list[:2]:
                subtotal = obat.harga_jual * 5
                DetailResep.objects.create(
                    resep=resep,
                    obat=obat,
                    jumlah_diminta=5,
                    dosis_aturan='3x sehari',
                    subtotal_harga=subtotal
                )
        
        self.stdout.write(self.style.SUCCESS('✓ Resep berhasil dibuat'))

    def seed_tagihan(self):
        self.stdout.write('💰 Membuat Tagihan...')
        
        kunjungan_list = Kunjungan.objects.all()
        kasir = Staff.objects.filter(jabatan='Kasir').first()
        metode_pembayaran = MetodePembayaran.objects.first()
        
        for i, kunjungan in enumerate(kunjungan_list):
            total_tindakan = Decimal('100000.00')
            total_obat = Decimal('50000.00')
            grand_total = total_tindakan + total_obat
            
            Tagihan.objects.create(
                nomor_invoice=f'INV-{timezone.now().strftime("%Y%m%d")}-{str(i+1).zfill(3)}',
                kunjungan=kunjungan,
                kasir=kasir,
                total_biaya_tindakan=total_tindakan,
                total_biaya_obat=total_obat,
                grand_total=grand_total,
                metode_bayar=metode_pembayaran,
                status_pembayaran='lunas',
                waktu_pembayaran=timezone.now()
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Tagihan berhasil dibuat'))

    def seed_loket(self):
        self.stdout.write('🪟 Membuat Loket...')
        
        staff_list = Staff.objects.filter(jabatan__in=['Perawat'])
        kunjungan = Kunjungan.objects.first()
        
        for i, staff in enumerate(staff_list):
            Loket.objects.create(
                nama_loket=f'Loket {i+1}',
                staff=staff,
                kunjungan=kunjungan if i == 0 else None
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Loket berhasil dibuat'))
