from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from seguridad.models import UserDetails

class DetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)

class RegistrarSerializer(serializers.ModelSerializer):
    detalles = DetalleSerializer()
    email = serializers.CharField(required=True, validators=[
                                  UniqueValidator(queryset=User.objects.all())])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2', 'detalles')
        extra_kwargs = {
            'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Las contraseñas no coinciden"}
            )
        return attrs

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        user = User.objects.create(
            username=validated_data['email'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        UserDetails.objects.create(usuario=user, **detalles_data)
        return user
