from django.contrib.auth.models import User
from django.db import models


class AlmacenamientoUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    asignado = models.FloatField(default=-1)
    usado = models.FloatField(default=0.0)
    comprado = models.FloatField(default=0.0)
    peso_archivo_asignado = models.FloatField(default=0.0)


class AlmacenamientoGlobal(models.Model):
    servidor = models.FloatField(default=-1)
    capacidad_max = models.FloatField(default=-1)
    peso_archivo_max = models.FloatField(default=-1)
    total_usado = models.FloatField(default=0.0)

