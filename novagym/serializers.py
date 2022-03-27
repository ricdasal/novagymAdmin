from rest_framework import serializers

from novagym.models import ProgresoImc


class ProgresoImcSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgresoImc
        fields = '__all__'
