from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from farmasi.models import Obat, KategoriObat

# ═════════════════════════════════════════════════════════════════════════════
# LIST & INDEX VIEW
# ═════════════════════════════════════════════════════════════════════════════

@login_required
def stok_obat_index(request):
    """
    Daftar stok obat dengan computed properties dari model.
    ✅ Tampilkan data dari @property computed values
    """
    daftar_obat = Obat.objects.select_related('kategori').all()
    
    # ✅ Hitung dari computed properties di model
    stok_rendah_list = [o for o in daftar_obat if o.stok_rendah]
    kadaluarsa_list = [o for o in daftar_obat if o.is_kadaluarsa]
    
    context = {
        'daftar_obat': daftar_obat,
        'stok_rendah_count': len(stok_rendah_list),
        'kadaluarsa_count': len(kadaluarsa_list),
        'total_nilai_stok': sum(o.nilai_stok for o in daftar_obat),
        'page_title': 'Stok Obat',
        'breadcrumbs': [
            {'name': 'Stok Obat', 'url': reverse('stok_obat_index')},
        ],
    }
    return render(request, 'pages/farmasi/stok_obat/index.html', context)

# ═════════════════════════════════════════════════════════════════════════════
# CREATE VIEW - AUTO CODE GENERATION
# ═════════════════════════════════════════════════════════════════════════════

@login_required
def stok_obat_create(request):
    """
    Buat obat baru.
    ✅ Kode auto-generate via EntityBase.generate_kode()
    ✅ Validation via EntityBase.validate_entity()
    """
    if request.method == "POST":
        try:
            # Input dari form
            nama_obat = request.POST.get('nama_obat', '').strip()
            kategori_id = request.POST.get('kategori')
            harga_beli = request.POST.get('harga_beli', '0')
            harga_jual = request.POST.get('harga', '0')
            satuan = request.POST.get('satuan', '').strip()
            tanggal_kadaluarsa = request.POST.get('tanggal_kadaluarsa')
            
            # Validasi basic input
            if not nama_obat:
                raise ValidationError("Nama obat tidak boleh kosong")
            if not kategori_id:
                raise ValidationError("Kategori harus dipilih")
            
            harga_beli_float = float(harga_beli) if harga_beli else 0
            harga_jual_float = float(harga_jual) if harga_jual else 0
            
            if harga_jual_float <= 0:
                raise ValidationError("Harga jual harus > 0")
            
            # ✅ Buat obat - kode akan auto-generate di save()
            obat = Obat(
                nama_obat=nama_obat,
                kategori_id=kategori_id,
                harga_beli=harga_beli_float,
                harga_jual=harga_jual_float,
                satuan=satuan,
                tanggal_kadaluarsa=tanggal_kadaluarsa if tanggal_kadaluarsa else None,
            )
            
            # ✅ save() akan:
            # 1. Call generate_kode() → auto-generate "OBT-xxxx"
            # 2. Call validate_entity() → validate business rules
            # 3. Raise ValidationError jika ada yang salah
            obat.save()
            
            messages.success(
                request,
                f'✅ Obat "{obat.nama_obat}" berhasil ditambahkan. Kode: {obat.kode_entity}'
            )
            return redirect('stok_obat_index')
            
        except ValueError as e:
            messages.error(request, f'❌ Input tidak valid: {str(e)}')
        except ValidationError as e:
            messages.error(request, f'❌ Data tidak valid: {str(e)}')
        except Exception as e:
            messages.error(request, f'❌ Terjadi kesalahan: {str(e)}')
    
    # GET request - tampilkan form
    kategori = KategoriObat.objects.filter(is_aktif=True).all()
    
    context = {
        'kategori_options': [(d.id, d.nama_kategori) for d in kategori],
        'page_title': 'Tambah Stok Obat',
        'breadcrumbs': [
            {'name': 'Stok Obat', 'url': reverse('stok_obat_index')},
            {'name': 'Tambah Stok', 'url': None},
        ],
    }
    
    return render(request, 'pages/farmasi/stok_obat/create.html', context)

# ═════════════════════════════════════════════════════════════════════════════
# EDIT VIEW - USE @PROPERTY SETTERS
# ═════════════════════════════════════════════════════════════════════════════

@login_required
def stok_obat_edit(request, id):
    """
    Edit obat.
    ✅ Gunakan @property setters yang auto-validate
    """
    obat = get_object_or_404(Obat, pk=id)
    
    if request.method == "POST":
        try:
            # ✅ Update via @property setters (auto-validate!)
            obat.nama_obat = request.POST.get('nama_obat', '').strip()
            
            harga_beli_val = request.POST.get('harga_beli', '0')
            harga_jual_val = request.POST.get('harga', '0')
            
            obat.harga_beli = float(harga_beli_val) if harga_beli_val else 0
            obat.harga_jual = float(harga_jual_val) if harga_jual_val else 0
            obat.satuan = request.POST.get('satuan', '').strip()
            obat.tanggal_kadaluarsa = request.POST.get('tanggal_kadaluarsa')
            obat.kategori_id = request.POST.get('kategori')
            
            # Validasi before save
            if not obat.nama_obat:
                raise ValidationError("Nama obat tidak boleh kosong")
            if obat.harga_jual <= 0:
                raise ValidationError("Harga jual harus > 0")
            
            # save() akan call validate_entity()
            obat.save()
            
            messages.success(request, f'✅ Obat berhasil diupdate')
            return redirect('stok_obat_index')
            
        except ValueError as e:
            messages.error(request, f'❌ Input tidak valid: {str(e)}')
        except ValidationError as e:
            messages.error(request, f'❌ Validasi gagal: {str(e)}')
        except Exception as e:
            messages.error(request, f'❌ Terjadi kesalahan: {str(e)}')
    
    # GET request - tampilkan form dengan data current
    kategori = KategoriObat.objects.filter(is_aktif=True).all()
    
    context = {
        'obat': obat,
        'kategori_options': [(d.id, d.nama_kategori) for d in kategori],
        'page_title': 'Edit Stok Obat',
        'breadcrumbs': [
            {'name': 'Stok Obat', 'url': reverse('stok_obat_index')},
            {'name': 'Edit Stok', 'url': None},
        ],
    }
    
    return render(request, 'pages/farmasi/stok_obat/edit.html', context)

# ═════════════════════════════════════════════════════════════════════════════
# STOK MANAGEMENT - CONTROLLED METHODS
# ═════════════════════════════════════════════════════════════════════════════

@login_required
def stok_obat_tambah(request, id):
    """
    Tambah stok obat.
    ✅ Gunakan controlled method: obat.tambah_stok()
    """
    obat = get_object_or_404(Obat, pk=id)
    
    if request.method == "POST":
        try:
            jumlah = int(request.POST.get('jumlah', 0))
            
            if jumlah <= 0:
                raise ValidationError("Jumlah harus > 0")
            
            # ✅ Gunakan controlled method
            obat.tambah_stok(jumlah)
            
            messages.success(
                request,
                f'✅ Stok {obat.nama_obat} ditambah {jumlah}. Total: {obat.stok}'
            )
            
        except ValueError:
            messages.error(request, '❌ Jumlah harus berupa angka')
        except ValidationError as e:
            messages.error(request, f'❌ {str(e)}')
        except Exception as e:
            messages.error(request, f'❌ Error: {str(e)}')
    
    return redirect('stok_obat_index')


@login_required
def stok_obat_kurangi(request, id):
    """
    Kurangi stok obat.
    ✅ Gunakan controlled method: obat.kurangi_stok()
    """
    obat = get_object_or_404(Obat, pk=id)
    
    if request.method == "POST":
        try:
            jumlah = int(request.POST.get('jumlah', 0))
            
            if jumlah <= 0:
                raise ValidationError("Jumlah harus > 0")
            
            # ✅ Gunakan controlled method
            obat.kurangi_stok(jumlah)
            
            messages.success(
                request,
                f'✅ Stok {obat.nama_obat} dikurangi {jumlah}. Total: {obat.stok}'
            )
            
        except ValueError:
            messages.error(request, '❌ Jumlah harus berupa angka')
        except ValidationError as e:
            messages.error(request, f'❌ Gagal kurangi stok: {str(e)}')
        except Exception as e:
            messages.error(request, f'❌ Error: {str(e)}')
    
    return redirect('stok_obat_index')


# ═════════════════════════════════════════════════════════════════════════════
# DELETE VIEW
# ═════════════════════════════════════════════════════════════════════════════

@login_required
def stok_obat_delete(request, id):
    """Delete obat"""
    try:
        obat = Obat.objects.get(id=id)
        nama_obat = obat.nama_obat
        obat.delete()
        messages.success(request, f'✅ Data obat "{nama_obat}" berhasil dihapus.')
    except Obat.DoesNotExist:
        messages.error(request, '❌ Data obat tidak ditemukan.')
    except Exception as e:
        messages.error(request, f'❌ Error: {str(e)}')
    
    return redirect('stok_obat_index')