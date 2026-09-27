from django.shortcuts import render, get_object_or_404
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from .models import Sesaun

def sesaun_lista(request):
    sesaun_sira = Sesaun.objects.all()
    return render(request, 'absensia/lista.html', {'sesaun_sira': sesaun_sira})

def sesaun_qr(request, pk):
    sesaun = get_object_or_404(Sesaun, pk=pk)
    # Generate unique QR token if not exists
    if not sesaun.kodigu_qr:
        sesaun.kodigu_qr = get_random_string(32)
        sesaun.save()
        
    return render(request, 'absensia/qr_display.html', {'sesaun': sesaun})

def api_refresh_qr(request, pk):
    sesaun = get_object_or_404(Sesaun, pk=pk)
    # Regenerate QR token
    sesaun.kodigu_qr = get_random_string(32)
    sesaun.save()
    
    return JsonResponse({
        'status': 'success',
        'token': sesaun.kodigu_qr
    })
