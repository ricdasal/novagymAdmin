from seguridad.models import UserDetails
from .models import Horario, HorarioReserva, MaquinaReserva,Posicion, PosicionMaquina, Zona,Maquina
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField,ImageField

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
    horario=PrimaryKeyRelatedField(queryset=Horario.objects.all())
    posicion=PrimaryKeyRelatedField(queryset=Posicion.objects.all())
    class Meta:
        model = HorarioReserva
        fields = ('id','codigo','horario', 'usuario','posicion')
    def create(self, validated_data):
            return HorarioReserva.objects.create(**validated_data)

class MaquinaSerializer(ModelSerializer):
    imagen=ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Maquina
        fields = ('id','codigo','nombre','descripcion','imagen','categoria','cantidad','reservable','activo','zona')
    def create(self, validated_data):
            return Maquina.objects.create(**validated_data)

class PosicionMaquinaSerializer(ModelSerializer):
    zona=ZonaSerializer(read_only=True, many=False)
    class Meta:
        model = PosicionMaquina
        fields = ('id','fila','coulmna','zona', 'ocupado')
    def create(self, validated_data):
            return PosicionMaquina.objects.create(**validated_data)  

class MaquinaReservaSerializer(ModelSerializer):
    usuario=PrimaryKeyRelatedField(queryset=UserDetails.objects.all())
    maquina=PrimaryKeyRelatedField(queryset=Maquina.objects.all())
    posicion=PrimaryKeyRelatedField(queryset=PosicionMaquina.objects.all())
    class Meta:
        model = MaquinaReserva
        fields = ('id','codigo','maquina', 'usuario','posicion','horario_inicio','horario_fin','fecha')
    def create(self, validated_data):
            return MaquinaReserva.objects.create(**validated_data)
