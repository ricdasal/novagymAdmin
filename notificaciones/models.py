from django.db import models

# Create your models here.
class Notificacion(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=24)
    cuerpo = models.CharField(max_length=255)
    imagen = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titulo

class NotificacionUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    def __str__(self):
        return str(self.sender_id) +"-"+ str(self.receiver_id)