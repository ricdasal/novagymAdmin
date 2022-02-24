from dataclasses import fields
from rest_framework import serializers
from decimal import Decimal
from almacenamiento.models import *
from .models import *


class BiografiaSerializer(serializers.ModelSerializer):
    usuario_info = serializers.ReadOnlyField()

    class Meta:
        model = Biografia
        fields = ['id', 'usuario', 'foto_perfil', 'foto_portada',
                 'descripcion', 'seguidores', 'usuario_info']


class ArchivoPublicacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArchivoPublicacion
        fields = ('id', 'archivo', 'tipo', 'almacenamiento_utilizado')
        

class PublicacionSerializer(serializers.ModelSerializer):
    usuario_info = serializers.ReadOnlyField()
    comentarios = serializers.ReadOnlyField()
    archivos = ArchivoPublicacionSerializer(many=True)

    class Meta:
        model = Publicacion
        fields = ['id', 'usuario', 'usuario_info', 'texto', 
                'fecha_creacion', 'num_likes', 'archivos', 'comentarios']

    def create(self, validated_data):
        archivos = validated_data.pop('archivos')
        publicacion = Publicacion.objects.create(**validated_data)
        for archivo in archivos:
            archivo = ArchivoPublicacion.objects.create(publicacion=publicacion, **archivo)
            archivo.aumentar_almacenamiento_usuario(publicacion.usuario)
            archivo.aumentar_almacenamiento_global()
        return publicacion
    
    def update(self, instance, validated_data):
        archivos = validated_data.pop('archivos')
        instance.texto = validated_data.get('texto', instance.texto)
        instance.save()
        for archivo in archivos:
            ArchivoPublicacion.objects.create(publicacion=instance, **archivo)
        return instance


class ComentarioSerializer(serializers.ModelSerializer):
    usuario_info = serializers.ReadOnlyField()
    comentarios_hijo = serializers.ReadOnlyField()
    es_padre = serializers.ReadOnlyField()

    class Meta:
        model = Comentario
        fields = ['id', 'texto', 'publicacion', 'usuario', 
                'usuario_info', 'fecha_creacion', 'imagen', 
                'comentario_padre', 'es_padre', 'comentarios_hijo']


class SeguidorSerializer(serializers.ModelSerializer):
    seguidor_info = serializers.ReadOnlyField()
    siguiendo = serializers.ReadOnlyField()

    class Meta:
        model = Seguidor
        fields = ['usuario', 'seguidor', 'seguidor_info', 'siguiendo']
        extra_kwargs = {"usuario": {"write_only": True, 'required': True}}

    def create(self, validated_data):
        seguidor = Seguidor.objects.create(**validated_data)
        return seguidor

class SeguidosSerializer(serializers.ModelSerializer):
    seguidos_info = serializers.ReadOnlyField()

    class Meta:
        model = Seguidor
        fields = ['usuario', 'seguidos_info']


class HistoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historia
        fields = ['id', 'usuario', 'texto', 
                'fecha_creacion', 'archivo', 'tipo_archivo']
        extra_kwargs = {"usuario": {"write_only": True, 'required': True}}