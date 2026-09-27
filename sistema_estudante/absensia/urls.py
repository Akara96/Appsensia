from django.urls import path
from . import views
from . import api_views

app_name = 'absensia'

urlpatterns = [
    path('sesaun/', views.sesaun_lista, name='sesaun_lista'),
    path('sesaun/<int:pk>/qr/', views.sesaun_qr, name='sesaun_qr'),
    path('sesaun/<int:pk>/qr/refresh/', views.api_refresh_qr, name='sesaun_qr_refresh'),
    
    # API Routes for Mobile App
    path('api/login/', api_views.api_login, name='api_login'),
    path('api/scan/', api_views.api_scan_qr, name='api_scan'),
]
