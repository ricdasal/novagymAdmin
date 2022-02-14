from django.db import models

# Create your models here.

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=24)
    imagen = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    class Talla(models.TextChoices):
        NA = 'NA', 'No aplica'
        EXTRA_SMALL = 'LS', 'Extra Small'
        SMALL = 'S', 'Small'
        MEDIUM = 'M', 'Medium'
        LARGE = 'L', 'Large'
        EXTRA_LARE = 'XL', 'Extra Large'
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=255, blank=True)
    nombre = models.CharField(max_length=24)
    descripcion = models.CharField(max_length=255)
    precio_referencial = models.DecimalField(max_digits=4, decimal_places=2)
    imagen = models.CharField(max_length=255, blank=True)
    categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE)
    valor_presentacion=models.DecimalField(max_digits=4, decimal_places=2)
    talla = models.CharField(max_length=3, choices=Talla.choices)
    unidad_presentacion = models.IntegerField()

    def __str__(self):
        return self.codigo + ' - ' + self.nombre


class Inventario(models.Model):
    id = models.AutoField(primary_key=True)
    precio = models.DecimalField(max_digits=4, decimal_places=2)
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    stock = models.IntegerField()
    def __str__(self):
        return self.nombre

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

    
class ProductoDescuento(models.Model):
    id = models.AutoField(primary_key=True)
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    porcentaje_descuento=models.DecimalField(max_digits=3,decimal_places=2)
    fecha_hora_desde=models.DateTimeField()
    fecha_hora_hasta=models.DateTimeField()
    estado=models.CharField(max_length=24)
    def __str__(self):
        return str(self.producto) +"-"+str(self.porcentaje_descuento)+"-"+ self.estado