from django import forms

class PasienForm(forms.Form):
    username = forms.CharField(max_length=150)
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    nik = forms.CharField(max_length=16)
    tanggal_lahir = forms.DateField()
    jenis_kelamin = forms.ChoiceField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    alamat = forms.CharField(widget=forms.Textarea)
    no_hp = forms.CharField(max_length=15)

class DokterForm(forms.Form):
    username = forms.CharField(max_length=150)
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    nomor_sip = forms.CharField(max_length=150)
    spesialisasi = forms.CharField(max_length=150)
    tarif_jasa = forms.IntegerField()
    no_hp = forms.CharField(max_length=15)
    alamat = forms.CharField(widget=forms.Textarea)

class StaffForm(forms.Form):
    username = forms.CharField(max_length=150)
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    jabatan = forms.CharField(max_length=150)
    shift_kerja = forms.CharField(max_length=150)
    no_hp = forms.CharField(max_length=15)
    alamat = forms.CharField(widget=forms.Textarea)

