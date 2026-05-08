from django import forms

class JadwalForm(forms.Form):
    dokter_id = forms.IntegerField()
    poli_id = forms.IntegerField()
    hari = forms.CharField(max_length=10)
    jam_mulai = forms.CharField(max_length=10)
    jam_selesai = forms.CharField(max_length=10)