from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField
from sponsor.models import Sucursal

class GimnasioSerializer(serializers.ModelSerializer):
    usuario=PrimaryKeyRelatedField(queryset=UserDetails.objects.all())
    sucursal=PrimaryKeyRelatedField(queryset=Sucursal.objects.all())
    class Meta:
        model = RegistroNovacoin
        fields = ('usuario','novacoins', 'sucursal','created_at')