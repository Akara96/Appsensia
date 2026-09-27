import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from estudante.models import Estudante
from absensia.models import Sesaun, Presensa

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                if hasattr(user, 'estudante'):
                    estudante = user.estudante
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Login susesu',
                        'data': {
                            'nre': estudante.nre,
                            'naran': f"{estudante.naran_primeiru} {estudante.naran_ikus}",
                            'departamentu': estudante.departamentu.kodigu if estudante.departamentu else ''
                        }
                    })
                else:
                    return JsonResponse({'status': 'error', 'message': 'Konta ne\'e laos estudante!'}, status=403)
            else:
                return JsonResponse({'status': 'error', 'message': 'Username ka Password sala!'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


@csrf_exempt
def api_scan_qr(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nre = data.get('nre')
            token = data.get('token')

            if not nre or not token:
                return JsonResponse({'status': 'error', 'message': 'Parametru la kompletu'}, status=400)

            estudante = Estudante.objects.filter(nre=nre).first()
            if not estudante:
                return JsonResponse({'status': 'error', 'message': 'Estudante la hetan'}, status=404)

            sesaun = Sesaun.objects.filter(kodigu_qr=token).first()
            if not sesaun:
                return JsonResponse({'status': 'error', 'message': 'Kódigu QR sala ka expire ona!'}, status=404)

            # Check if already present
            if Presensa.objects.filter(sesaun=sesaun, estudante=estudante).exists():
                return JsonResponse({'status': 'error', 'message': 'Ita halo presensa ona ba sesaun ne\'e!'}, status=409)

            # Mark presence
            Presensa.objects.create(
                sesaun=sesaun,
                estudante=estudante,
                status='Prezente'
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Presensa Susesu!',
                'data': {
                    'kadeira': sesaun.kadeira,
                    'dosente': sesaun.dosente.naran
                }
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
