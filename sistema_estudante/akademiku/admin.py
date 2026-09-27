from django.contrib import admin
from .models import Departamentu, Dosente, SalaDeAula

@admin.register(Departamentu)
class DepartamentuAdmin(admin.ModelAdmin):
    list_display = ('kodigu', 'naran')
    search_fields = ('kodigu', 'naran')

@admin.register(Dosente)
class DosenteAdmin(admin.ModelAdmin):
    list_display = ('nid', 'naran', 'departamentu', 'status')
    list_filter = ('departamentu', 'status')
    search_fields = ('nid', 'naran')

@admin.register(SalaDeAula)
class SalaDeAulaAdmin(admin.ModelAdmin):
    list_display = ('naran', 'kapasidade', 'fatin')
    list_filter = ('fatin',)
    search_fields = ('naran',)
