from importlib.metadata import requires
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import User

from backend.settings import BASE_DIR
from .models import *
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.serializers import Serializer, TimeField,FileField, CharField,URLField, PrimaryKeyRelatedField, DateField, BooleanField, EmailField

class SucursalSerializer(ModelSerializer):
    imagen= FileField(required=False)
    class Meta:
        model = Sponsor
        fields = ('id','codigo', 'direccion', 'nombre', 'telefono','celular','imagen','horario_apertura','horario_cierre','correo')

class SponsorSerializer(ModelSerializer):
    sucursal_set = SucursalSerializer(read_only=True, many=True)
    imagen=FileField(required=False)
    class Meta:
        model = Sponsor
        fields = ('id', 'nombre','direccion','correo','es_matriz', 'descripcion', 'telefono','celular', 'nombre_contacto', 'url','red_social','imagen','fecha_inicio','fecha_fin',"activo",'horario_apertura','horario_cierre','sucursal_set')
