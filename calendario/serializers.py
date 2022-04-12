from django.contrib.auth.models import User
from gimnasio.models import Gimnasio

from seguridad.models import UserDetails
from .models import Horario, HorarioReserva,Posicion, Zona
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

class ZonaSerializer(ModelSerializer):
    class Meta:
        model = Zona
        fields = ('id','nombre','espacios', 'tipo')
    def create(self, validated_data):
            return Zona.objects.create(**validated_data)

class PosicionSerializer(ModelSerializer):
    zona=ZonaSerializer(read_only=True, many=False)
    class Meta:
        model = Posicion
        fields = ('id','posicion','zona', 'ocupado')
    def create(self, validated_data):
            return Zona.objects.create(**validated_data)            

class HorarioSerializer(ModelSerializer):
    #zona=ZonaSerializer(read_only=True, many=False)
    gimnasio=PrimaryKeyRelatedField(many=False,read_only=True)
    class Meta:
        model = Horario
        fields = ('id','dia','nombre', 'descripcion','horario_inicio', 'horario_fin','gimnasio','capacidad','asistentes','activo','zona')
    def create(self, validated_data):
            return Horario.objects.create(**validated_data)

class HorarioReservaSerializer(ModelSerializer):
    usuario=PrimaryKeyRelatedField(queryset=UserDetails.objects.all())
    horario=HorarioSerializer(read_only=True, many=False)
    posicion=PosicionSerializer(read_only=True, many=False)
    class Meta:
        model = HorarioReserva
        fields = ('id','codigo','horario', 'usuario','posicion')
    def create(self, validated_data):
            return HorarioReserva.objects.create(**validated_data)