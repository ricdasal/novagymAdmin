from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from gimnasio.models import Gimnasio
from seguridad.models import UserDetails
from seguridad.validators import (validate_decimal_positive,
                                  validate_decimal_positive_include)

# Create your models here.


class Beneficio(models.Model):
    nombre = models.CharField(max_length=255)
    texto = models.TextField()

    def __str__(self):
        return self.nombre


class Membresia(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                 validate_decimal_positive])
    dias_duracion = models.PositiveIntegerField(
        validators=[validate_decimal_positive_include], blank=True)
    meses_duracion = models.PositiveIntegerField(
        validators=[validate_decimal_positive_include], blank=True)
    beneficios = models.ManyToManyField(Beneficio, related_name='membresia')
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='membresia/', null=True, blank=True)
    acceso_todo = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pk']

    @property
    def descuento_activo(self):
        try:
            return self.descuentos.get(activo=True).porcentaje_descuento
        except:
            return 0

    def __str__(self):
        return self.nombre


class Descuento(models.Model):
    membresia = models.ForeignKey(
        Membresia, related_name='descuentos', on_delete=models.SET_NULL, null=True)
    porcentaje_descuento = models.PositiveIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    fecha_hora_desde = models.DateTimeField()
    fecha_hora_hasta = models.DateTimeField()
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.membresia.nombre + ' - %' + str(self.porcentaje_descuento)


class Historial(models.Model):
    usuario = models.ForeignKey(
        UserDetails, on_delete=models.SET_NULL, null=True, related_name='historial_membresia')
    membresia = models.ForeignKey(
        Membresia, on_delete=models.SET_NULL, null=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    costo = models.DecimalField(max_digits=12, decimal_places=2)
    activa = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gimnasio = models.ForeignKey(Gimnasio, on_delete=models.SET_NULL, null=True, blank=True)
    pagoRecurrente = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.nombres + ' - ' + self.membresia.nombre
