from django.db import models

class Departamentu(models.Model):
    naran = models.CharField(max_length=100, verbose_name="Naran Departamentu")
    kodigu = models.CharField(max_length=10, unique=True, verbose_name="Kódigu")
    deskrisaun = models.TextField(blank=True, null=True, verbose_name="Deskrisaun")

    class Meta:
        verbose_name_plural = "Departamentu Sira"
        ordering = ['naran']

    def __str__(self):
        return f"{self.kodigu} - {self.naran}"

class Dosente(models.Model):
    STATUS_CHOICES = (
        ('Ativu', 'Ativu'),
        ('La Ativu', 'La Ativu'),
    )
    naran = models.CharField(max_length=150, verbose_name="Naran Kompletu")
    nid = models.CharField(max_length=20, unique=True, verbose_name="NID (Númeru Identifikasaun Dosente)")
    departamentu = models.ForeignKey(Departamentu, on_delete=models.CASCADE, related_name="dosente_sira", verbose_name="Departamentu")
    email = models.EmailField(blank=True, null=True)
    telemovel = models.CharField(max_length=15, blank=True, null=True, verbose_name="Nu. Telemovel")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ativu')

    class Meta:
        verbose_name_plural = "Dosente Sira"
        ordering = ['naran']

    def __str__(self):
        return f"{self.nid} - {self.naran}"

class SalaDeAula(models.Model):
    naran = models.CharField(max_length=50, verbose_name="Naran Sala")
    kapasidade = models.IntegerField(verbose_name="Kapasidade")
    fatin = models.CharField(max_length=100, blank=True, null=True, verbose_name="Fatin / Bloku")
    deskrisaun = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Sala De Aula Sira"
        ordering = ['naran']

    def __str__(self):
        return self.naran
