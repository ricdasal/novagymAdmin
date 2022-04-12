from django.contrib.auth.models import User

from seguridad.models import UserDetails
from .models import Horario, HorarioReserva,Posicion, Zona
from rest_framework.serializers import Serializer, PrimaryKeyRelatedField

class HorarioSerializer(Serializer):

    class Meta:
        model = Horario
        fields = ('id','dia','nombre', 'descripcion','horario_inicio', 'horario_fin','gimnasio')

class HorarioReservaSerializer(Serializer):
    usuario=PrimaryKeyRelatedField(queryset=UserDetails.objects.all())
    horario=PrimaryKeyRelatedField(queryset=Horario.objects.all())
    posicion=PrimaryKeyRelatedField(queryset=Posicion.objects.all())
    class Meta:
        model = HorarioReserva
        fields = ('horario', 'usuario','posicion')
    def create(self, validated_data):
            return HorarioReserva.objects.create(**validated_data)

class ZonaSerializer(Serializer):
    class Meta:
        model = Zona
        fields = ('id','nombre','espacio', 'tipo')
    def create(self, validated_data):
            return Zona.objects.create(**validated_data)