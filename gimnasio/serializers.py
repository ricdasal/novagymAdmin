from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers

class GimnasioSerializer(serializers.ModelSerializer):
    imagen = serializers.FileField(required=False)
    class Meta:
        model = Gimnasio
        fields = ('id','nombre'
        , 'imagen','telefono','celular','ubicacion'
        ,'horario_inicio', 'horario_fin'
        ,'estado','ciudad','aforo','capacidad','personas',
        'latitud','longitud')