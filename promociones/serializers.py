from django.contrib.auth.models import User
from .models import Promociones
from rest_framework import serializers

class PublicidadSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Promociones
        fields = ('titulo', 'fecha_hora_inicio', 'fecha_hora_fin','correo', 'imagen','descripcion','activo','telefono','celular','nombre_contacto','url')
