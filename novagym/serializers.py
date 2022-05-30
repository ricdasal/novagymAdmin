from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from membresia.models import Historial
from rest_framework import serializers

from novagym.models import (DetalleTransaccionMembresia,
                            DetalleTransaccionProducto,
                            ObjetivoPeso,
                            ProgresoImc,
                            Transaccion)


class ProgresoImcSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgresoImc
        fields = "__all__"


class ObjetivoPesoSerializer(serializers.ModelSerializer):
    progreso_imc = ProgresoImcSerializer(many=True, read_only=True)
    peso = serializers.CharField(write_only=True)
    estatura = serializers.CharField(write_only=True)

    class Meta:
        model = ObjetivoPeso
        fields = [
            'id',
            'usuario',
            'fecha_inicio',
            'fecha_fin',
            'titulo',
            'estado',
            'peso',
            'estatura',
            'progreso_imc',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        if 'fecha_inicio' in attrs and 'fecha_fin' in attrs:
            if attrs['fecha_inicio'] >= attrs['fecha_fin']:
                raise serializers.ValidationError(
                    {"fecha_inicio": "Fecha de inicio no puede ser igual o mayor a la fecha de fin"})
        return attrs

    def create(self, validated_data):
        peso = Decimal(validated_data.pop('peso'))
        estatura = Decimal(validated_data.pop('estatura'))
        usuario = validated_data.get('usuario')
        imc = {'peso': peso, 'estatura': estatura,
               'usuario': usuario}
        objetivo = super().create(validated_data)
        ProgresoImc.objects.create(objetivo=objetivo, **imc)
        return objetivo


"""
revisar desde aqui
"""


class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = '__all__'


class DetalleTransaccionMembresiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleTransaccionMembresia
        exclude = ('dias', 'meses')


class DetalleTransaccionProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleTransaccionProducto
        exclude = ('nombre', 'total')


class TransaccionProductoSerializer(serializers.ModelSerializer):
    transaccion_producto = DetalleTransaccionProductoSerializer(many=True)

    class Meta:
        model = Transaccion
        fields = ['id',
                  'usuario',
                  'nombre_user',
                  'auth_code',
                  'id_tramite',
                  'subtotal',
                  'descuento',
                  'iva',
                  'valor_total',
                  'estado',
                  'transaccion_producto',
                  ]

    def create(self, validated_data):
        detalles_data = validated_data.pop('transaccion_producto')
        transaccion = Transaccion.objects.create(**validated_data)
        for producto in detalles_data:
            DetalleTransaccionProducto.objects.create(
                transaccion=transaccion, **producto)
        transaccion.save()
        return transaccion

    def update(self, instance, validated_data):
        detalles_data = []
        if 'transaccion_producto' in validated_data:
            detalles_data = validated_data.pop('transaccion_producto')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.transaccion_producto.all().delete()
        for producto in detalles_data:
            DetalleTransaccionProducto.objects.create(
                transaccion=instance, **producto)
        instance.save()
        return instance


class TransaccionMembresiaSerializer(serializers.ModelSerializer):
    transaccion_membresia = DetalleTransaccionMembresiaSerializer(many=True)
    gimnasio = serializers.CharField(write_only=True,required=False)

    class Meta:
        model = Transaccion
        fields = ['id',
                  'usuario',
                  'nombre_user',
                  'auth_code',
                  'id_tramite',
                  'subtotal',
                  'descuento',
                  'iva',
                  'valor_total',
                  'estado',
                  'transaccion_membresia',
                  'gimnasio',
                  ]

    def create(self, validated_data):
        detalles_data = validated_data.pop('transaccion_membresia')
        gimnasio = validated_data.pop('gimnasio') if 'gimnasio' in validated_data else None
        transaccion = Transaccion.objects.create(**validated_data)

        for membresia_data in detalles_data:
            DetalleTransaccionMembresia.objects.create(
                transaccion=transaccion, **membresia_data)
        transaccion.save()

        membresia = transaccion.transaccion_membresia.all()[0].membresia
        fecha_inicio = timezone.now()
        usuario = transaccion.usuario.detalles
        
        if usuario.tiene_membresia:
            current_membresia = usuario.membresia
            current_membresia.activa = False
            current_membresia.save()
        Historial.objects.create(
            usuario=usuario,
            membresia=membresia,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_inicio +
            relativedelta(months=membresia.dias_duracion,
                          days=membresia.meses_duracion),
            costo=membresia.precio,
            activa=True,
            gimnasio_id=gimnasio)
        return transaccion

    def update(self, instance, validated_data):
        detalles_data = []
        if 'transaccion_membresia' in validated_data:
            detalles_data = validated_data.pop('transaccion_membresia')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.transaccion_membresia.all().delete()
        for producto in detalles_data:
            DetalleTransaccionMembresia.objects.create(
                transaccion=instance, **producto)
        instance.save()
        return instance
