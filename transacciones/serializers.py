from decimal import Decimal
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from membresia.models import Historial
from rest_framework import serializers
from .models import (Transaccion, DetalleTransaccion)

class DetalleTransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleTransaccion
        exclude = ('usuario',
                  'valor_total',
                  'descuento',
                  'subtotal',
                  'iva',
                  'auth_code',
                  'id_tramite',
                  'estado')


class TransaccionSerializer(serializers.ModelSerializer):
    detalle = DetalleTransaccionSerializer(many=True)

    class Meta:
        model = Transaccion
        fields = ['usuario',
                  'valor_total',
                  'descuento',
                  'subtotal',
                  'iva',
                  'auth_code',
                  'id_tramite',
                  'estado',
                  'detalle',
                  ]
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalle')
        transaccion = Transaccion.objects.create(**validated_data)
        pre = str(transaccion.pk)
        sec = '0'*(9-len(pre))+pre
        transaccion.codigo = sec
        for producto in detalles_data:
            DetalleTransaccion.objects.create(transaccion=transaccion, **producto)
        transaccion.save()
        return transaccion

    def update(self, instance, validated_data):
        detalles_data = []
        if 'detalle' in validated_data:
            detalles_data = validated_data.pop('detalle')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.detalle.all().delete()
        for producto in detalles_data:
            DetalleTransaccion.objects.create(
                transaccion=instance, **producto)
        instance.save()
        return instance



