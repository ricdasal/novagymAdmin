from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
class Transaccion(models.Model):
    class Estado(models.TextChoices):
        NOPAG = 'NPG', 'Pendiente de Pago'
        CANCEL = 'CNC', 'Anulada'
        PAID = 'PAG', 'Pagada'
        DES = 'DES', 'Despachada'

    codigo = models.CharField(max_length=64, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    auth_code = models.CharField(max_length=10)
    id_tramite = models.CharField(max_length=20)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=24, choices=Estado.choices, default=Estado.NOPAG)
    created_at = models.DateTimeField(auto_now_add=True)
    

class DetalleTransaccion(models.Model):
    transaccion = models.ForeignKey(Transaccion, on_delete=models.SET_NULL, null=True, related_name='detalle')   
    categoria = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()
    precio = models.CharField(max_length=5)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    usaNovacoins = models.BooleanField()
