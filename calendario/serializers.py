from gimnasio.serializers import GimnasioSerializer,GimnasioSmallSerializer
from seguridad.models import UserDetails
from seguridad.serializers import UsuarioDetallesSerializer
from .models import Horario, HorarioMaquina, HorarioReserva, MaquinaReserva,Posicion, PosicionMaquina, Zona,Maquina
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField,ImageField,CharField,FileField

class ZonaSerializer(ModelSerializer):
    class Meta:
        model = Zona
        fields = ('id','nombre','espacios', 'tipo')
    def create(self, validated_data):
            return Zona.objects.create(**validated_data)

class PosicionSerializer(ModelSerializer):
    class Meta:
        model = Posicion
        fields = ('id','posicion','zona', 'ocupado')
    def create(self, validated_data):
            return Posicion.objects.create(**validated_data)   

class ZonaHorarioSerializer(ModelSerializer):
    posiciones=PosicionSerializer(read_only=True, many=True)
    class Meta:
        model = Zona
        fields = ('id','nombre','espacios', 'tipo','posiciones')
    def create(self, validated_data):
            return Zona.objects.create(**validated_data)         

class HorarioSerializer(ModelSerializer):
    #zona=ZonaSerializer(read_only=True, many=False)
    gimnasio=PrimaryKeyRelatedField(many=False,read_only=True)
    class Meta:
        model = Horario
        fields = ('id','nombre', 'descripcion','gimnasio','capacidad','asistentes','activo','zona')
    def create(self, validated_data):
            return Horario.objects.create(**validated_data)

class HorarioReservaSerializer(ModelSerializer):
    #usuario=UsuarioDetallesSerializer(read_only=True, many=False)
    #horario=HorarioSerializer(read_only=True, many=False)
    #posicion=PosicionSerializer(read_only=True, many=False)
    class Meta:
        model = HorarioReserva
        fields = ('id','codigo','clase','fecha','horario','usuario','posicion','created_at')
    def create(self, validated_data):
            return HorarioReserva.objects.create(**validated_data)

class MaquinaSerializer(ModelSerializer):
    imagen=FileField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Maquina
        fields = ('id','codigo','nombre','descripcion','imagen','categoria','cantidad','reservable','activo','zona','gimnasio')
    def create(self, validated_data):
            return Maquina.objects.create(**validated_data)

class PosicionMaquinaSerializer(ModelSerializer):
    zona=ZonaSerializer(read_only=True, many=False)
    class Meta:
        model = PosicionMaquina
        fields = ('id','fila','columna','zona', 'ocupado')
    def create(self, validated_data):
            return PosicionMaquina.objects.create(**validated_data)  

class MaquinaReservaSerializer(ModelSerializer):
    usuario=PrimaryKeyRelatedField(queryset=UserDetails.objects.all())
    maquina=PrimaryKeyRelatedField(queryset=Maquina.objects.all())
    posicion=PrimaryKeyRelatedField(queryset=PosicionMaquina.objects.all())
    class Meta:
        model = MaquinaReserva
        fields = ('id','codigo','maquina', 'usuario','posicion','horario','fecha','gimnasio')
    def create(self, validated_data):
            return MaquinaReserva.objects.create(**validated_data)

class MaquinaDispoSerializer(ModelSerializer):
    imagen=ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    zona=ZonaSerializer(read_only=True, many=False)
    posiciones=PosicionMaquinaSerializer(read_only=True, many=True)
    class Meta:
        model = Maquina
        fields = ('codigo','nombre','descripcion','imagen','categoria','cantidad','reservable','activo','zona','gimnasio','posiciones')
    def create(self, validated_data):
            return Maquina.objects.create(**validated_data)

class HorarioDispoSerializer(ModelSerializer):
    zona=ZonaHorarioSerializer(read_only=True, many=False)
    gimnasio=GimnasioSerializer(read_only=True, many=False)
    class Meta:
        model = Horario
        fields = ('id','dia','nombre', 'descripcion','horario_inicio', 'horario_fin','gimnasio','capacidad','asistentes','activo','zona')
    def create(self, validated_data):
            return Horario.objects.create(**validated_data)

class ReporteHorarioReservaSerializer(ModelSerializer):
    usuario=CharField(read_only=True)
    horario_nombre=CharField(source="horario",read_only=True)
    posicion_posicion=CharField(source="posicion",read_only=True)
    class Meta:
        model = HorarioReserva
        fields = ('id','codigo','horario_nombre', 'usuario','posicion_posicion')
    def create(self, validated_data):
            return HorarioReserva.objects.create(**validated_data)

class ReporteMaquinaReservaSerializer(ModelSerializer):
    usuario=CharField(read_only=True)
    maquina=CharField(read_only=True)
    posicion=CharField(read_only=True)
    class Meta:
        model = MaquinaReserva
        fields = ('id','codigo','maquina', 'usuario','posicion','horario_inicio','horario_fin','fecha','gimnasio')
    def create(self, validated_data):
            return MaquinaReserva.objects.create(**validated_data)

class HorarioSmallSerializer(ModelSerializer):
    gimnasio=GimnasioSmallSerializer(read_only=True, many=False)
    class Meta:
        model=Horario
        fields=('id','nombre','horario_inicio','horario_fin','gimnasio')

class HorarioMaquinaSerializer(ModelSerializer):
    maquina=MaquinaSerializer(read_only=True,many=False)
    class Meta:
        model=HorarioMaquina
        fields=('id','maquina','horario_inicio','horario_fin')

class HorarioHorarioSerializer(ModelSerializer):
    horario=HorarioSerializer(read_only=True,many=False)
    class Meta:
        model=HorarioMaquina
        fields=('id','horario','horario_inicio','horario_fin')