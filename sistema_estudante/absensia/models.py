from django.db import models
from akademiku.models import Dosente, SalaDeAula
from estudante.models import Estudante

class Sesaun(models.Model):
    kadeira = models.CharField(max_length=150, verbose_name="Kadeira / Matéria")
    dosente = models.ForeignKey(Dosente, on_delete=models.CASCADE, related_name="sesaun_sira", verbose_name="Dosente")
    sala = models.ForeignKey(SalaDeAula, on_delete=models.SET_NULL, null=True, related_name="sesaun_sira", verbose_name="Sala de Aula")
    data = models.DateField(verbose_name="Data Sesaun")
    tempu_hahu = models.TimeField(verbose_name="Tempu Hahú")
    tempu_remata = models.TimeField(verbose_name="Tempu Remata")
    deskrisaun = models.TextField(blank=True, null=True, verbose_name="Deskrisaun / Tópiku")
    kodigu_qr = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name="Kódigu QR (Token)")

    class Meta:
        verbose_name_plural = "Sesaun Sira (Jadwal Kelas)"
        ordering = ['-data', '-tempu_hahu']

    def __str__(self):
        return f"{self.kadeira} - {self.data} ({self.tempu_hahu})"

class Presensa(models.Model):
    STATUS_CHOICES = (
        ('Prezente', 'Prezente'),
        ('Falla', 'Falla (Alfa)'),
        ('Lisensa', 'Lisensa (Ijin)'),
        ('Moras', 'Moras (Sakit)'),
    )

    sesaun = models.ForeignKey(Sesaun, on_delete=models.CASCADE, related_name="presensa_sira", verbose_name="Sesaun")
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name="presensa_sira", verbose_name="Estudante")
    tempu_tama = models.DateTimeField(auto_now_add=True, verbose_name="Tempu Tama (Scan)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Prezente', verbose_name="Status Absensi")

    class Meta:
        verbose_name_plural = "Presensa Sira (Data Absensi)"
        unique_together = ('sesaun', 'estudante') # Saun estudante ida bele halo presensa dala ida deit ba sesaun ida
        ordering = ['-tempu_tama']

    def __str__(self):
        return f"{self.estudante.nre} - {self.sesaun.kadeira} ({self.status})"
