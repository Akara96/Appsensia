import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'konfigurasaun.settings')
django.setup()

from akademiku.models import Departamentu
from django.contrib.auth.models import User

# Buat Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fect.untl.edu.tl', 'admin123')
    print("Superuser 'admin' kria ona ho password 'admin123'")

# Data Departamentu FECT UNTL
departamentu_sira = [
    {'kodigu': 'ECV', 'naran': 'Engenharia Civil'},
    {'kodigu': 'EMC', 'naran': 'Engenharia Mecânica'},
    {'kodigu': 'EEE', 'naran': 'Engenharia Eletrónica e Elétrica'},
    {'kodigu': 'EINF', 'naran': 'Engenharia Informática'},
    {'kodigu': 'EGP', 'naran': 'Engenharia Geologia e Petróleo'},
]

print("Hahu hatama data departamentu FECT UNTL...")
for dep in departamentu_sira:
    obj, created = Departamentu.objects.get_or_create(
        kodigu=dep['kodigu'],
        defaults={'naran': dep['naran']}
    )
    if created:
        print(f"  + Kria Departamentu: {obj.kodigu} - {obj.naran}")
    else:
        print(f"  * Departamentu {obj.kodigu} eziste ona")

print("Susesu! Data master hotu hatama ona.")
