from django.db import models
from django.contrib.auth.models import User
from akademiku.models import Departamentu

class Estudante(models.Model):
    JENIS_KELAMIN = (
        ('M', 'Mane'),
        ('F', 'Feto'),
    )
    STATUS_CHOICES = (
        ('Ativu', 'Ativu'),
        ('La Ativu', 'La Ativu'),
        ('Graduadu', 'Graduadu'),
    )

    uza_nain = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='estudante', verbose_name="Konta Uza-Na'in")
    nre = models.CharField(max_length=20, unique=True, verbose_name="NRE (Númeru Rejistu Estudante)")
    naran_primeiru = models.CharField(max_length=100, verbose_name="Naran Primeiru")
    naran_ikus = models.CharField(max_length=100, verbose_name="Naran Ikus")
    jeneru = models.CharField(max_length=1, choices=JENIS_KELAMIN, verbose_name="Jéneru")
    fatin_moris = models.CharField(max_length=100, verbose_name="Fatin Moris")
    data_moris = models.DateField(verbose_name="Data Moris")
    hela_fatin = models.TextField(verbose_name="Hela Fatin")
    telefoni = models.CharField(max_length=15, verbose_name="Telefoni")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    foto = models.ImageField(upload_to='foto_estudante/', blank=True, null=True, verbose_name="Foto")
    
    departamentu = models.ForeignKey(Departamentu, on_delete=models.SET_NULL, null=True, related_name='estudante_sira', verbose_name="Departamentu")
    tinan_tama = models.IntegerField(verbose_name="Tinan Tama")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ativu', verbose_name="Status")

    class Meta:
        verbose_name_plural = "Estudante Sira"
        ordering = ['-tinan_tama', 'naran_primeiru']

    def __str__(self):
        return f"{self.nre} - {self.naran_primeiru} {self.naran_ikus}"
