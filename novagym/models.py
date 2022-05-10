from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from membresia.models import Membresia
from productos.models import Producto
from seguridad.models import UserDetails


class ObjetivoPeso(models.Model):
    class Meta:
        ordering = ["-created_at"]

    usuario = models.ForeignKey(
        UserDetails, on_delete=models.CASCADE, related_name="objetivo_peso")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    titulo = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class ProgresoImc(models.Model):
    class Meta:
        ordering = ["-created_at"]

    usuario = models.ForeignKey(
        UserDetails, on_delete=models.CASCADE)
    objetivo = models.ForeignKey(
        ObjetivoPeso, on_delete=models.CASCADE, related_name="progreso_imc")
    peso = models.DecimalField(max_digits=5, decimal_places=2)  # kilogramos
    estatura = models.DecimalField(max_digits=5, decimal_places=2)  # metros
    resultado = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calcular_imc(self):
        resultado = self.peso/(self.estatura**2)
        return resultado

    def save(self, *args, **kwargs):
        self.resultado = self.calcular_imc()
        return super().save(*args, **kwargs)


class TipoPago(models.Model):
    nombre = models.CharField(max_length=24)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Transaccion(models.Model):
    class Estado(models.TextChoices):
        NOPAG = 'NPG', 'Pendiente de Pago'
        CANCEL = 'CNC', 'Anulada'
        PAID = 'PAG', 'Pagada'
        DES = 'DES', 'Despachada'

    codigo = models.CharField(max_length=64, blank=True)
    usuario     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    nombre_user = models.CharField(max_length=50)
    auth_code   = models.CharField(max_length=20)
    id_tramite  = models.CharField(max_length=30)
    subtotal    = models.DecimalField(max_digits=10, decimal_places=2)
    descuento   = models.DecimalField(max_digits=10, decimal_places=2)
    iva         = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado      = models.CharField(max_length=24, choices=Estado.choices, default=Estado.NOPAG)
    created_at  = models.DateTimeField(auto_now_add=True)
    

class DetalleTransaccionMembresia(models.Model):
    transaccion = models.ForeignKey(  Transaccion, on_delete=models.SET_NULL, null=True, related_name='transaccion_membresia')
    membresia   = models.ForeignKey(  Membresia,   on_delete=models.SET_NULL, null=True)
    categoria   = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    dias        = models.PositiveIntegerField()
    meses       = models.PositiveIntegerField()
    cantidad    = models.PositiveIntegerField()
    precio      = models.DecimalField(max_digits=12, decimal_places=2)
    total       = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.dias = self.membresia.dias_duracion
        self.meses = self.membresia.meses_duracion
        return super().save(*args, **kwargs)



class DetalleTransaccionProducto(models.Model):
    transaccion     = models.ForeignKey( Transaccion, on_delete=models.SET_NULL, null=True, related_name='transaccion_producto')
    producto        = models.ForeignKey(    Producto, on_delete=models.SET_NULL, null=True)
    categoria       = models.CharField(max_length=20)
    descripcion     = models.CharField(max_length=50)
    nombre          = models.CharField(max_length=24, unique=True)
    cantidad        = models.PositiveIntegerField()
    precio          = models.DecimalField(max_digits=12, decimal_places=2)
    total           = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.nombre = self.producto.nombre
        return super().save(*args, **kwargs)
