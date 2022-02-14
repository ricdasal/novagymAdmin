from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers


class SponsorSerializer(serializers.ModelSerializer):
    nombre=serializers.CharField(max_length=24)
    descripcion = serializers.CharField(max_length=255)
    telefono = serializers.CharField(max_length=12)
    nombre_contacto = serializers.CharField(max_length=24)
    url = serializers.CharField(max_length=255)
    imagen = serializers.CharField(max_length=255)
    class Meta:
        model = Sponsor
        fields = ('id', 'nombre', 'descripcion', 'telefono', 'nombre_contacto', 'url','imagen')

class NotificacionSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(max_length=24)
    cuerpo = serializers.CharField(max_length=255)
    imagen = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField()
    class Meta:
        model = Notificacion
        fields = ('id', 'titulo', 'cuerpo', 'imagen', 'created_at')

class NotificacionUsuarioSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField()
    receiver_id = serializers.IntegerField()
    class Meta:
        model = NotificacionUsuario
        fields = ('id','sender_id', 'receiver_id')

class InventarioSerializer(serializers.ModelSerializer):
    precio = serializers.DecimalField(max_digits=4, decimal_places=2)
    producto_id=serializers.IntegerField()
    stock = serializers.IntegerField()
    class Meta:
        model = Inventario
        fields = ('id','precio','producto_id', 'stock')

class CategoriaSerializer(serializers.ModelSerializer):
    nombre = models.CharField(max_length=24)
    imagen = models.CharField(max_length=255)
    class Meta:
        model = Categoria
        fields = ('id','nombre','imagen')

class ProductoSerializer(serializers.ModelSerializer):
    codigo = serializers.CharField(max_length=255)
    nombre = serializers.CharField(max_length=24)
    descripcion = serializers.CharField(max_length=255)
    precio_referencial = serializers.DecimalField(max_digits=4, decimal_places=2)
    imagen = serializers.CharField(max_length=255)
    categoria_id=serializers.IntegerField()
    valor_presentacion=serializers.DecimalField(max_digits=4, decimal_places=2)
    talla = serializers.CharField(max_length=3)
    unidad_presentacion = serializers.IntegerField()
    class Meta:
        model = Producto
        fields = ('id','codigo','nombre', 'descripcion','precio_referencial','imagen','categoria_id', 'valor_presentacion','talla','unidad_presentacion')



class ProductoDescuentoSerializer(serializers.ModelSerializer):
    producto_id=serializers.IntegerField()
    porcentaje_descuento=serializers.DecimalField(max_digits=3,decimal_places=2)
    fecha_hora_desde=serializers.DateTimeField()
    fecha_hora_hasta=serializers.DateTimeField()
    estado=serializers.CharField()
    class Meta:
        model = ProductoDescuento
        fields = ('id','producto_id','porcentaje_descuento', 'fecha_hora_desde','fecha_hora_hasta','estado')