from django.db import models
from usuarios.models import Pacientes

class Gravacoes(models.Model):
    video = models.FileField(upload_to='gravacoes')
    data = models.DateTimeField()
    transcrever = models.BooleanField(default=False)
    paciente = models.ForeignKey(Pacientes, on_delete=models.DO_NOTHING)
    humor = models.IntegerField(default=0)
    transcricao = models.TextField()
    resumo = models.JSONField(default=list, blank=True)
    segmentos = models.JSONField(default=list, blank=True)
    # rag = models.JSONField(default=dict, blank=True)