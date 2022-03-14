from django.db import models

# Create your models here.

class Gimnasio(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=24)
    nombre = models.CharField(max_length=24)
    imagen = models.ImageField(upload_to="gimnasios/", null=True, blank=True)
    telefono = models.CharField(max_length=24)
    ubicacion = models.CharField(max_length=24)
    horario_inicio = models.TimeField(blank=False)
    horario_fin = models.TimeField(blank=False)
    estado = models.BooleanField(default=True)
    ciudad = models.CharField(max_length=24)
    aforo = models.PositiveIntegerField()
    def __str__(self):
        return self.nombre +"-"+self.ciudad