from django.contrib.auth.models import User
from django.db import models


class AlmacenamientoUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    asignado = models.DecimalField(max_digits=10, decimal_places=2 ,default=-1)
    usado = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    comprado = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    peso_archivo_asignado = models.DecimalField(max_digits=10, decimal_places=2 ,default=-1)


class AlmacenamientoGlobal(models.Model):
    servidor = models.DecimalField(max_digits=10, decimal_places=2 ,default=-1)
    capacidad_max = models.DecimalField(max_digits=10, decimal_places=2 ,default=-1)#lo max que puede tener un usuario de almacenamiento
    peso_archivo_max = models.DecimalField(max_digits=10, decimal_places=2 ,default=-1)
    total_usado = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)

