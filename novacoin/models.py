from django.contrib.auth.models import User
from django.db import models
from novagym.models import Transaccion

# Create your models here.


class Cartera(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    saldo_coins = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)


class MotivoCanje(models.Model):
    class Tipo(models.TextChoices):
        INGRESO = 'IN', 'Ingreso'
        EGRESO = 'OUR', 'Egreso'
    nombre = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    tipo_movimiento = models.CharField(
        max_length=4, choices=Tipo.choices, default=Tipo.INGRESO)


class DetalleCartera(models.Model):
    class Meta:
        ordering = ['-updated_at']
    cartera = models.ForeignKey(Cartera, on_delete=models.SET_NULL, null=True)
    transaccion = models.ForeignKey(
        Transaccion, on_delete=models.SET_NULL, null=True, blank=True)
    motivo_canje = models.ForeignKey(
        MotivoCanje, on_delete=models.SET_NULL, null=True)
    coins_egreso = models.DecimalField(max_digits=10, decimal_places=2)
    coins_ingreso = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RangoCambioCoins(models.Model):
    texto = models.CharField(max_length=255)
    monto_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    monto_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    coins = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)
    motivo = models.ForeignKey(
        MotivoCanje, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)