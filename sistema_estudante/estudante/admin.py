from django.contrib import admin
from .models import Estudante

@admin.register(Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ('nre', 'naran_primeiru', 'naran_ikus', 'departamentu', 'tinan_tama', 'status')
    list_filter = ('departamentu', 'tinan_tama', 'status', 'jeneru')
    search_fields = ('nre', 'naran_primeiru', 'naran_ikus')
    fieldsets = (
        ('Konta Uza-Na\'in', {
            'fields': ('uza_nain',)
        }),
        ('Informasaun Pessoal', {
            'fields': ('nre', 'naran_primeiru', 'naran_ikus', 'jeneru', 'fatin_moris', 'data_moris', 'foto')
        }),
        ('Kontaktu', {
            'fields': ('hela_fatin', 'telefoni', 'email')
        }),
        ('Akadémiku', {
            'fields': ('departamentu', 'tinan_tama', 'status')
        }),
    )
