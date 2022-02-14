from django.db import models

# Create your models here.

class Sponsor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=24)
    descripcion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=12)
    nombre_contacto = models.CharField(max_length=24)
    url = models.CharField(max_length=255)
    imagen = models.CharField(max_length=255)
    def __str__(self):
        return str(self.sender_id) +"-"+ str(self.receiver_id)