from django.contrib.auth.models import Group, User
from django.db import models
from django.dispatch import receiver

# Create your models here.


class Notificacion(models.Model):
    class Meta:
        ordering = ['-created_at']

    class Frecuencia(models.TextChoices):
        D1 = 'D1', 'Una vez al dia'
        S1 = 'S1', 'Una vez a la semana'
        S2 = 'S2', 'Dos veces a la semana'
        M1 = 'M1', 'Una vez al mes'
        M2 = 'M2', 'Dos veces al mes'
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    cuerpo = models.TextField()
    imagen = models.ImageField(
        upload_to='notificacion/', null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    frecuencia = models.CharField(
        max_length=3, choices=Frecuencia.choices, default="S1")
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class NotificacionUsuario(models.Model):
    class Meta:
        ordering = ['-created_at']

    notificacion = models.ForeignKey(
        Notificacion, on_delete=models.SET_NULL, null=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='emisor')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receptor', blank=True, null=True)
    grupo_usuarios = models.ForeignKey(
        Group, blank=True, on_delete=models.SET_NULL, null=True, related_name="receptores")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        receptor = self.receiver.username if self.receiver else self.grupo_usuarios.name
        return self.sender.username + "-> " + receptor
