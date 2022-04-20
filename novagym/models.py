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
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=24, choices=Estado.choices, default=Estado.NOPAG)
    tipo_pago = models.ForeignKey(
        TipoPago, on_delete=models.SET_NULL, null=True)


class DetalleTransaccionMembresia(models.Model):
    transaccion = models.ForeignKey(
        Transaccion, on_delete=models.SET_NULL, null=True, related_name='transaccion_membresia')
    membresia = models.ForeignKey(
        Membresia, on_delete=models.SET_NULL, null=True)
    meses = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.PositiveIntegerField()
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def calcular_subtotal(self):
        return self.precio * Decimal(1 - self.descuento/100)

    def calcular_iva(self):
        return self.subtotal * Decimal(1.12)

    def save(self, *args, **kwargs):
        self.meses = self.membresia.meses_duracion
        self.precio = self.membresia.precio
        self.descuento = self.membresia.descuento_activo
        self.subtotal = self.calcular_subtotal()
        self.iva = self.calcular_iva()
        self.total = self.subtotal + self.iva
        return super().save(*args, **kwargs)


class DetalleTransaccionProducto(models.Model):
    transaccion = models.ForeignKey(
        Transaccion, on_delete=models.SET_NULL, null=True, related_name='transaccion_producto')
    producto = models.ForeignKey(
        Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.PositiveIntegerField()
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def calcular_subtotal(self):
        return self.cantidad * (self.precio * Decimal(1 - self.descuento/100))

    def calcular_iva(self):
        return self.subtotal * Decimal(1.12)

    def save(self, *args, **kwargs):
        self.descuento = self.producto.descuento_activo
        self.subtotal = self.calcular_subtotal()
        self.iva = self.calcular_iva()
        self.total = self.subtotal + self.iva
        return super().save(*args, **kwargs)
