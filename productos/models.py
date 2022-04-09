import random

from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=24)
    imagen = models.ImageField(upload_to="categoriasProductos/",
                               null=True, blank=True, default="images/no_image.png")
                               
    class Meta:
        ordering=('-id',)
    def __str__(self):
        return self.nombre


def generarCodigo():
    not_unique = True
    while not_unique:
        unique_code = "PDT-"+str(random.randint(1000, 9999))
        if not Producto.objects.filter(codigo=unique_code):
            not_unique = False
            return str(unique_code)


class Producto(models.Model):
    class Talla(models.TextChoices):
        NA = 'NA', 'No aplica'
        EXTRA_SMALL = 'XS', 'Extra Small'
        SMALL = 'S', 'Small'
        MEDIUM = 'M', 'Medium'
        LARGE = 'L', 'Large'
        EXTRA_LARE = 'XL', 'Extra Large'

    class Presentacion(models.TextChoices):
        NA = 'No aplica', 'No aplica'
        Embalaje = 'Embalaje', 'Embalaje'
        Caja = 'Caja', 'Caja'
        Recipiente = 'Recipiente', 'Recipiente'
        Enfundado = 'Enfundado', 'Enfundado'
        Lata = 'Lata', 'Lata'
        Botella = 'Botella', 'Botella'

    id = models.AutoField(primary_key=True)
    codigo = models.CharField(
        max_length=20, unique=True, default=generarCodigo, editable=False)
    nombre = models.CharField(max_length=24, unique=True)
    descripcion = models.CharField(max_length=130)
    imagen=models.ImageField(upload_to="productos/", null=False, blank=False,default="images/no_image.png")
    categoria=models.ForeignKey(Categoria, on_delete=models.PROTECT)
    talla = models.CharField(max_length=3, choices=Talla.choices)
    presentacion = models.CharField(
        max_length=10, choices=Presentacion.choices)
    usaNovacoins = models.BooleanField()
    class Meta:
        ordering=('-id',)
    @property
    def descuento_activo(self):
        try:
            return self.descuentos.get(estado=True).porcentaje_descuento
        except:
            return 0

    def __str__(self):
        return self.codigo + ' - ' + self.nombre


class Inventario(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    precioCompra = models.DecimalField(
        max_digits=4, decimal_places=2, default=0)
    stock = models.PositiveIntegerField()
    novacoins = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre


class ProductoDescuento(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='descuentos')
    porcentaje_descuento = models.PositiveIntegerField()
    fecha_hora_desde = models.DateTimeField()
    fecha_hora_hasta = models.DateTimeField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return str(self.producto) + "-"+str(self.porcentaje_descuento)+"-" + self.estado
