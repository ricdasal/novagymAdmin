from django.contrib.auth.models import User
from drf_extra_fields.fields import Base64ImageField
from membresia.serializers import HistorialSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from seguridad.models import UserDetails


class UsuarioDetallesSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='usuario.email')
    membresia = serializers.SerializerMethodField()
    seguidores = serializers.CharField(
        source='usuario.biografia.seguidores', read_only=True)
    seguidos = serializers.CharField(
        source='usuario.biografia.seguidos', read_only=True)
    novacoins = serializers.CharField(
        source='usuario.cartera.saldo_coins', read_only=True)
    imagen = Base64ImageField(
        allow_empty_file=True, required=False, allow_null=True)

    class Meta:
        model = UserDetails
        fields = ['id', 'email', 'codigo', 'cedula', 'membresia', 'nombres', 'apellidos', 'imagen',
                  'telefono', 'sexo', 'tipo', 'fecha_nacimiento', 'seguidores', 'seguidos', 'novacoins',
                  'added_by', 'created_at', 'updated_at', "created_from"]

    def get_membresia(self, object):
        try:
            membresia_serializer = HistorialSerializer(
                object.membresia, context={'request': self.context['request']}).data
            return membresia_serializer
        except:
            return None

    def update(self, instance, validated_data):
        if "usuario" in validated_data:
            new_email = validated_data.pop('usuario')['email']
            if new_email != instance.usuario.email:
                # TODO: Agregar funciones para reenviar correo de ser necesario. OJO
                print("Email ha cambiado. Enviar correo")
                instance.usuario.email = new_email
                instance.usuario.username = new_email
                instance.usuario.save()
        return super().update(instance, validated_data)


class DetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        exclude = ['usuario', 'imagen']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)


class RegistrarSerializer(serializers.ModelSerializer):
    detalles = DetalleSerializer()
    email = serializers.CharField(required=True, validators=[
                                  UniqueValidator(queryset=User.objects.all())])
    password2 = serializers.CharField(write_only=True, required=True)
    imagen = Base64ImageField(
        allow_empty_file=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2', 'imagen', 'detalles')
        extra_kwargs = {
            'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Las contraseñas no coinciden"})
        return attrs

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        # extract imagen from data and readd to detalles_data.
        if "imagen" in validated_data:
            imagen = validated_data.pop('imagen')
            detalles_data['imagen'] = imagen
        user = User.objects.create(
            username=validated_data['email'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        try:
            pre = str(int(UserDetails.objects.latest('pk').pk+1))
            sec = '0'*(4-len(pre))+pre
        except self.model.DoesNotExist:
            sec = '0001'
        detalles_data['codigo'] = sec
        UserDetails.objects.create(usuario=user, **detalles_data)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['old_password'] == attrs['password']:
            raise serializers.ValidationError(
                {"password": "Su contraseña es la misma que la anterior"})
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "La nueva contraseña no coincide"})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Su anterior contraseña no es correcta"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
