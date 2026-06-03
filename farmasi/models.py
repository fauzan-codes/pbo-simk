from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
from accounts.models import TimestampModel

# ═════════════════════════════════════════════════════════════════════════════
# ABSTRAKSI: Abstract Base Class mendefinisikan kontrak
# ═════════════════════════════════════════════════════════════════════════════

class EntityBase(TimestampModel):
    """
    ABSTRAKSI: Abstract base class untuk entities dengan kode auto-generated.
    
    Mendefinisikan interface/contract yang harus diimplementasikan subclass:
    - generate_kode() - Generate unique code untuk entity
    - validate_entity() - Validate business rules per entity type
    """
    
    kode_entity = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        db_index=True,
        help_text="Auto-generated unique code"
    )
    deskripsi = models.TextField(blank=True)
    is_aktif = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        """
        POLIMORFISME: Template method pattern.
        Define skeleton, let subclass implement generate_kode() & validate_entity()
        """
        if not self.kode_entity:
            self.kode_entity = self.generate_kode()
        
        self.validate_entity()  # Call polymorphic method
        super().save(*args, **kwargs)
    
    def generate_kode(self):
        """
        ABSTRAKSI: Abstract method - must be implemented by subclass.
        Each entity type has different code generation logic.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} harus implement generate_kode()"
        )
    
    def validate_entity(self):
        """
        ABSTRAKSI: Abstract method - must be implemented by subclass.
        Each entity type has different validation rules.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} harus implement validate_entity()"
        )
    
    def __str__(self):
        """POLIMORFISME: String representation untuk admin."""
        return f"[{self.kode_entity}] {self.deskripsi[:50] if self.deskripsi else self.__class__.__name__}"


# ═════════════════════════════════════════════════════════════════════════════
# INHERITANCE & POLIMORFISME: KategoriObat
# ═════════════════════════════════════════════════════════════════════════════

class KategoriObat(EntityBase):
    """
    Pharmaceutical category with full OOP implementation.
    
    INHERITANCE: Mewarisi dari EntityBase → TimestampModel
    ENKAPSULASI: Private field dengan validation
    ABSTRAKSI: Implement abstract methods
    POLIMORFISME: Override generate_kode, validate_entity, __str__
    """
    
    # ENKAPSULASI: Private field dengan underscore
    _nama_kategori = models.CharField(
        max_length=100,
        db_column='nama_kategori',
        help_text="Private field - access via @property"
    )
    
    class Meta:
        db_table = 'kategori_obat'
        verbose_name_plural = 'Kategori Obat'
        permissions = [
            ('can_manage_kategori', 'Can manage kategori obat'),
        ]
    
    # ─── ENKAPSULASI: Getter untuk nama_kategori ───
    @property
    def nama_kategori(self):
        """Readonly access to nama_kategori via property."""
        return self._nama_kategori
    
    @nama_kategori.setter
    def nama_kategori(self, value):
        """Setter dengan validasi business logic."""
        if not value or not value.strip():
            raise ValidationError("Nama kategori tidak boleh kosong")
        if len(value) < 3:
            raise ValidationError("Nama kategori minimal 3 karakter")
        self._nama_kategori = value
    
    # ─── POLIMORFISME: Implement abstract method generate_kode ───
    def generate_kode(self):
        """
        POLIMORFISME: Implementation unique untuk KategoriObat.
        Format: KAT-xxxx
        """
        prefix = "KAT"
        last_kategori = KategoriObat.objects.all().order_by('-id').first()
        
        if last_kategori and last_kategori.kode_entity:
            try:
                last_num = int(last_kategori.kode_entity.split('-')[1])
                new_num = last_num + 1
            except (IndexError, ValueError):
                new_num = 1
        else:
            new_num = 1
        
        return f"{prefix}-{str(new_num).zfill(4)}"
    
    # ─── POLIMORFISME: Implement abstract method validate_entity ───
    def validate_entity(self):
        """POLIMORFISME: Validation logic unique untuk KategoriObat."""
        if not self._nama_kategori or not self._nama_kategori.strip():
            raise ValidationError("Nama kategori tidak boleh kosong")
        
        # Check duplicate (excluding self)
        exists = KategoriObat.objects.exclude(pk=self.pk).filter(
            _nama_kategori__iexact=self._nama_kategori
        ).exists()
        
        if exists:
            raise ValidationError(f"Kategori '{self._nama_kategori}' sudah ada")
    
    # ─── POLIMORFISME: Override __str__ ───
    def __str__(self):
        """POLIMORFISME: Custom string representation."""
        return f"[{self.kode_entity}] {self._nama_kategori}"
    
    # ─── ENKAPSULASI: Business logic methods ───
    @property
    def jumlah_obat(self):
        """ENKAPSULASI: Computed property - count aktif obat."""
        return self.obat_set.filter(is_aktif=True).count()
    
    def deactivate(self):
        """ENKAPSULASI: Controlled method untuk deactivate."""
        self.is_aktif = False
        self.save()


# ═════════════════════════════════════════════════════════════════════════════
# INHERITANCE & POLIMORFISME: Obat
# ═════════════════════════════════════════════════════════════════════════════

class Obat(EntityBase):
    """
    Pharmaceutical product with full OOP implementation.
    
    INHERITANCE: Mewarisi dari EntityBase
    ENKAPSULASI: Private stok field dengan getter/setter + validation
    ABSTRAKSI: Implement abstract methods
    POLIMORFISME: Override methods dengan logic unik
    """
    
    nama_obat = models.CharField(max_length=255, db_index=True)
    kategori = models.ForeignKey(KategoriObat, on_delete=models.CASCADE)
    satuan = models.CharField(max_length=20)
    
    # ENKAPSULASI: Private field untuk stok
    _stok = models.PositiveIntegerField(
        db_column='stok',
        default=0,
        help_text="Private field - akses via @property"
    )
    
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2)
    harga_beli = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tanggal_kadaluarsa = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'obat'
        unique_together = ('kode_entity', 'kategori')
        permissions = [
            ('can_manage_stok', 'Can manage stok obat'),
            ('can_view_harga', 'Can view harga obat'),
        ]
    
    # ═════════════════════════════════════════════════════════════════════════
    # ENKAPSULASI: Stok Management dengan getter/setter
    # ═════════════════════════════════════════════════════════════════════════
    
    @property
    def stok(self):
        """ENKAPSULASI: Getter - Readonly access to stok."""
        return self._stok
    
    @stok.setter
    def stok(self, value):
        """ENKAPSULASI: Setter - Validate before assign."""
        if not isinstance(value, int):
            raise ValidationError("Stok harus berupa angka bulat")
        if value < 0:
            raise ValidationError("Stok tidak boleh negatif")
        self._stok = value
    
    # ─── ENKAPSULASI: Controlled methods untuk modify stok ───
    def tambah_stok(self, jumlah, catatan=""):
        """ENKAPSULASI: Controlled method untuk tambah stok."""
        if jumlah <= 0:
            raise ValidationError("Jumlah penambahan harus positif")
        
        self._stok += jumlah
        self.save()
    
    def kurangi_stok(self, jumlah, catatan=""):
        """ENKAPSULASI: Controlled method untuk kurangi stok."""
        if jumlah <= 0:
            raise ValidationError("Jumlah pengurangan harus positif")
        
        if jumlah > self._stok:
            raise ValidationError(
                f"Stok tidak cukup! Stok saat ini: {self._stok}, "
                f"diminta: {jumlah}"
            )
        
        self._stok -= jumlah
        self.save()
    
    # ═════════════════════════════════════════════════════════════════════════
    # ENKAPSULASI: Computed Properties
    # ═════════════════════════════════════════════════════════════════════════
    
    @property
    def stok_rendah(self):
        """ENKAPSULASI: Computed property - is stock low?"""
        MINIMUM_STOK = 10
        return self._stok < MINIMUM_STOK
    
    @property
    def nilai_stok(self):
        """ENKAPSULASI: Computed property - total stok value."""
        return self._stok * self.harga_jual
    
    @property
    def margin_keuntungan(self):
        """ENKAPSULASI: Computed property - profit margin %."""
        if not self.harga_beli or self.harga_beli == 0:
            return 0
        return ((self.harga_jual - self.harga_beli) / self.harga_beli) * 100
    
    @property
    def is_kadaluarsa(self):
        """ENKAPSULASI: Computed property - is medicine expired?"""
        if not self.tanggal_kadaluarsa:
            return False
        return date.today() > self.tanggal_kadaluarsa
    
    # ─── POLIMORFISME: Implement abstract method generate_kode ───
    def generate_kode(self):
        """
        POLIMORFISME: Implementation unique untuk Obat.
        Format: OBT-xxxx (berbeda dari KategoriObat yang KAT-xxxx)
        """
        prefix = "OBT"
        last_obat = Obat.objects.all().order_by('-id').first()
        
        if last_obat and last_obat.kode_entity:
            try:
                last_num = int(last_obat.kode_entity.split('-')[1])
                new_num = last_num + 1
            except (IndexError, ValueError):
                new_num = 1
        else:
            new_num = 1
        
        return f"{prefix}-{str(new_num).zfill(4)}"
    
    # ─── POLIMORFISME: Implement abstract method validate_entity ───
    def validate_entity(self):
        """POLIMORFISME: Validation logic unique untuk Obat."""
        if not self.nama_obat or not self.nama_obat.strip():
            raise ValidationError("Nama obat tidak boleh kosong")
        
        if not self.kategori_id:
            raise ValidationError("Kategori obat harus dipilih")
        
        if self.harga_jual <= 0:
            raise ValidationError("Harga jual harus lebih dari 0")
        
        if self.is_kadaluarsa:
            raise ValidationError(f"Obat sudah kadaluarsa pada {self.tanggal_kadaluarsa}")
        
        if self.harga_beli and self.harga_jual < self.harga_beli:
            raise ValidationError("Harga jual tidak boleh kurang dari harga beli")
    
    # ─── POLIMORFISME: Override __str__ ───
    def __str__(self):
        """POLIMORFISME: Custom string representation dengan status."""
        status = "⚠️ RENDAH" if self.stok_rendah else "✓ OK"
        return f"[{self.kode_entity}] {self.nama_obat} ({status})"
    
    # ─── POLIMORFISME: Override clean untuk validasi model ───
    def clean(self):
        """POLIMORFISME: Validasi sebelum save."""
        super().clean()
        self.validate_entity()


# ═════════════════════════════════════════════════════════════════════════════
# INHERITANCE & POLIMORFISME: Resep
# ═════════════════════════════════════════════════════════════════════════════

class Resep(EntityBase):
    """
    Medical prescription with full OOP implementation.
    
    INHERITANCE: Mewarisi dari EntityBase
    ENKAPSULASI: Private status field
    ABSTRAKSI: Implement abstract methods
    POLIMORFISME: Override methods dengan logic unik
    """
    
    rekam_medis = models.ForeignKey('pelayanan.RekamMedis', on_delete=models.CASCADE)
    apoteker = models.ForeignKey('accounts.Staff', on_delete=models.SET_NULL, null=True)
    
    # ENKAPSULASI: Status dengan choices
    _status = models.CharField(
        max_length=20,
        db_column='status',
        choices=[('diproses', 'Diproses'), ('selesai', 'Selesai'), ('dibatalkan', 'Dibatalkan')],
        default='diproses'
    )
    
    tanggal_resep = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'resep'
        permissions = [
            ('can_approve_resep', 'Can approve resep'),
            ('can_cancel_resep', 'Can cancel resep'),
        ]
    
    # ─── ENKAPSULASI: Getter untuk status ───
    @property
    def status(self):
        """ENKAPSULASI: Readonly access to status."""
        return self._status
    
    @status.setter
    def status(self, value):
        """ENKAPSULASI: Setter dengan validasi."""
        allowed = ['diproses', 'selesai', 'dibatalkan']
        if value not in allowed:
            raise ValidationError(f"Status harus salah satu dari: {allowed}")
        self._status = value
    
    # ─── POLIMORFISME: Implement abstract method generate_kode ───
    def generate_kode(self):
        """
        POLIMORFISME: Implementation unique untuk Resep.
        Format: RPT-yyyymmdd-xxxx (include tanggal)
        """
        prefix = f"RPT-{timezone.now().strftime('%Y%m%d')}"
        today_resep = Resep.objects.filter(
            kode_entity__startswith=prefix
        ).order_by('-kode_entity').first()
        
        if today_resep:
            last_num = int(today_resep.kode_entity.split('-')[-1])
            new_num = str(last_num + 1).zfill(4)
        else:
            new_num = "0001"
        
        return f"{prefix}-{new_num}"
    
    # ─── POLIMORFISME: Implement abstract method validate_entity ───
    def validate_entity(self):
        """POLIMORFISME: Validation logic unique untuk Resep."""
        if not self.rekam_medis:
            raise ValidationError("Resep harus terkait dengan rekam medis")
        if not self.apoteker:
            raise ValidationError("Apoteker harus ditentukan")
    
    # ─── POLIMORFISME: Override __str__ ───
    def __str__(self):
        """POLIMORFISME: Custom string representation."""
        return f"[{self.kode_entity}] Resep - {self.get__status_display()}"
    
    # ─── ENKAPSULASI: Business logic methods ───
    def approve(self):
        """ENKAPSULASI: Controlled method untuk approve resep."""
        if self._status != 'diproses':
            raise ValidationError("Hanya resep dengan status 'diproses' yang bisa disetujui")
        self._status = 'selesai'
        self.save()
    
    def cancel(self):
        """ENKAPSULASI: Controlled method untuk cancel resep."""
        if self._status == 'selesai':
            raise ValidationError("Resep yang sudah selesai tidak bisa dibatalkan")
        self._status = 'dibatalkan'
        self.save()


# ═════════════════════════════════════════════════════════════════════════════
# INHERITANCE & POLIMORFISME: DetailResep
# ═════════════════════════════════════════════════════════════════════════════

class DetailResep(TimestampModel):
    """
    Prescription detail with OOP implementation.
    
    INHERITANCE: Mewarisi dari TimestampModel
    ENKAPSULASI: Private jumlah field
    POLIMORFISME: Override save() dengan business logic
    """
    
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE)
    obat = models.ForeignKey(Obat, on_delete=models.CASCADE)
    
    # ENKAPSULASI: Private field untuk jumlah
    _jumlah_diminta = models.PositiveIntegerField(
        db_column='jumlah_diminta',
        help_text="Private field - akses via @property"
    )
    
    dosis_aturan = models.CharField(max_length=100)
    subtotal_harga = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    
    class Meta:
        db_table = 'detail_resep'
        unique_together = ('resep', 'obat')
    
    # ─── ENKAPSULASI: Getter untuk jumlah_diminta ───
    @property
    def jumlah_diminta(self):
        """ENKAPSULASI: Getter - Readonly access."""
        return self._jumlah_diminta
    
    @jumlah_diminta.setter
    def jumlah_diminta(self, value):
        """ENKAPSULASI: Setter dengan validasi."""
        if value <= 0:
            raise ValidationError("Jumlah diminta harus lebih dari 0")
        self._jumlah_diminta = value
    
    # ─── ENKAPSULASI: Computed properties ───
    @property
    def harga_satuan(self):
        """ENKAPSULASI: Computed property - harga satuan dari obat."""
        return self.obat.harga_jual
    
    @property
    def stok_tersedia(self):
        """ENKAPSULASI: Computed property - check stok tersedia."""
        return self.obat.stok >= self._jumlah_diminta
    
    # ─── POLIMORFISME: Override save() dengan business logic ───
    def save(self, *args, **kwargs):
        """
        POLIMORFISME: Override save() dengan custom preprocessing.
        - Auto-calculate subtotal_harga
        - Validate stok tersedia
        - Validate jumlah positif
        """
        # Auto-calculate subtotal
        self.subtotal_harga = self._jumlah_diminta * self.obat.harga_jual
        
        # Validate stok cukup
        if self._jumlah_diminta > self.obat.stok:
            raise ValidationError(
                f"Stok {self.obat.nama_obat} tidak cukup. "
                f"Diminta: {self._jumlah_diminta}, Tersedia: {self.obat.stok}"
            )
        
        super().save(*args, **kwargs)
    
    # ─── POLIMORFISME: Override __str__ ───
    def __str__(self):
        """POLIMORFISME: Custom string representation."""
        return f"{self.resep.kode_entity} - {self.obat.nama_obat} ({self._jumlah_diminta})"