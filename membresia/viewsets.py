from rest_framework import permissions, viewsets

from membresia.models import Beneficio, Descuento, Historial, Membresia
from membresia.serializers import (BeneficioSerializer, DescuentoSerializer,
                                   HistorialSerializer, MembresiaSerializer)


class HistorialMemebresiaViewset(viewsets.ModelViewSet):
    serializer_class = HistorialSerializer
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Historial.objects.filter(
            usuario=self.request.user.detalles).prefetch_related(
            'usuario', 'membresia').order_by('-created_at')
        return queryset


class MembresiaViewSet(viewsets.ModelViewSet):
    serializer_class = MembresiaSerializer

    def get_queryset(self):
        queryset = Membresia.objects.filter(
            estado=True).prefetch_related('beneficios', 'descuentos')
        return queryset


class BeneficioViewSet(viewsets.ModelViewSet):
    queryset = Beneficio.objects.all().order_by('id')
    serializer_class = BeneficioSerializer


class DescuentoViewSet(viewsets.ModelViewSet):
    queryset = Descuento.objects.all().order_by('-activo')
    serializer_class = DescuentoSerializer
