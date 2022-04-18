from decimal import Decimal
from re import I

from rest_framework import serializers

from novagym.models import ObjetivoPeso, ProgresoImc


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
