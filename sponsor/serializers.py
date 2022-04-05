from backend.settings import BASE_DIR
from .models import *
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ImageField

class SucursalSerializer(ModelSerializer):
    imagen= ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Sucursal
        fields = ('id','codigo', 'direccion', 'nombre', 'telefono','celular','imagen','sponsor','horario_apertura','horario_cierre','correo',"activo",'fecha_inicio','fecha_fin')

class SponsorSerializer(ModelSerializer):
    sucursal_set = SucursalSerializer(read_only=True, many=True)
    imagen=ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Sponsor
        fields = ('id', 'nombre','direccion','correo','es_matriz', 'descripcion', 'telefono','celular', 'nombre_contacto', 'url','red_social','imagen','fecha_inicio','fecha_fin',"activo",'horario_apertura','horario_cierre','sucursal_set')
