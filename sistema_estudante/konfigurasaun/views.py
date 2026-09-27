from django.shortcuts import render
from estudante.models import Estudante
from akademiku.models import Dosente
from absensia.models import Sesaun
from datetime import date

def painel_view(request):
    total_estudante = Estudante.objects.count()
    total_dosente = Dosente.objects.count()
    
    ohin = date.today()
    sesaun_sira = Sesaun.objects.filter(data=ohin)
    total_sesaun_ohin = sesaun_sira.count()

    context = {
        'total_estudante': total_estudante,
        'total_dosente': total_dosente,
        'total_sesaun_ohin': total_sesaun_ohin,
        'sesaun_sira': sesaun_sira,
    }
    return render(request, 'painel/index.html', context)
