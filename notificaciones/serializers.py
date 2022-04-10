from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class NotificacionSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(max_length=24)
    cuerpo = serializers.CharField(max_length=255)
    imagen = serializers.FileField(required=False)
    created_at = serializers.DateTimeField()

    class Meta:
        model = Notificacion
        fields = ('id', 'titulo', 'cuerpo', 'imagen', 'created_at')


class NotificacionUsuarioSerializer(serializers.ModelSerializer):
    notificacion = NotificacionSerializer()
    publicacion = serializers.IntegerField(
        source='notificacion.notificacion_publicacion.publicacion.id', read_only=True)

    class Meta:
        model = NotificacionUsuario
        fields = ('id', 'notificacion', 'publicacion')
