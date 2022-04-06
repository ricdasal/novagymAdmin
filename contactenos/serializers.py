from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import Serializer, ImageField, CharField, PrimaryKeyRelatedField

from seguridad.models import UserDetails
from .models import Buzon

class BuzonSerializer(serializers.ModelSerializer):
    sender=PrimaryKeyRelatedField(queryset=UserDetails.objects.all())
    titulo=CharField()
    descripcion=CharField()
    imagen=ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Buzon
        fields = ['sender','titulo','descripcion','imagen']