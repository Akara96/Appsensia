from django.contrib import admin
from .models import Sesaun, Presensa

class PresensaInline(admin.TabularInline):
    model = Presensa
    extra = 1
    autocomplete_fields = ['estudante']

@admin.register(Sesaun)
class SesaunAdmin(admin.ModelAdmin):
    list_display = ('kadeira', 'dosente', 'sala', 'data', 'tempu_hahu', 'tempu_remata')
    list_filter = ('data', 'dosente', 'sala')
    search_fields = ('kadeira', 'kodigu_qr')
    inlines = [PresensaInline]
    date_hierarchy = 'data'

@admin.register(Presensa)
class PresensaAdmin(admin.ModelAdmin):
    list_display = ('estudante', 'sesaun', 'tempu_tama', 'status')
    list_filter = ('status', 'sesaun__data')
    search_fields = ('estudante__nre', 'estudante__naran_primeiru', 'sesaun__kadeira')
    autocomplete_fields = ['estudante', 'sesaun']
