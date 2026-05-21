from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def resep_obat_index(request):
    context = {
        'page_title': 'Resep Obat'
    }

    return render(
        request,
        'pages/pelayanan/resep_obat/index.html',
        context
    )