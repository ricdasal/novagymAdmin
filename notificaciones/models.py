from django.db import models

# Create your models here.
class Notificacion(models.Model):
    class Frecuencia(models.TextChoices):
        D1 = 'D1', 'Una vez al dia'
        S1 = 'S1', 'Una vez a la semana'
        S2 = 'S2', 'Dos veces a la semana'
        M1 = 'M1', 'Una vez al mes'
        M2 = 'M2', 'Dos veces al mes'
        EN = 'EN', 'Envio realizado'
        PE = 'PE', 'Pedido listo'
        RE = 'RE', 'Recordatorio de reserva'
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=24)
    cuerpo = models.CharField(max_length=255)
    imagen=models.ImageField(upload_to="notificaciones/", null=True, blank=True,default="images/no_image.png")
    fecha_hora_inicio= models.DateTimeField()
    fecha_hora_fin= models.DateTimeField()
    frecuencia = models.CharField(max_length=3, choices=Frecuencia.choices)
    activo= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo

class NotificacionUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    def __str__(self):
        return str(self.sender_id) +"-"+ str(self.receiver_id)