from rest_framework import permissions, viewsets

from novagym.models import ObjetivoPeso, ProgresoImc
from novagym.serializers import ObjetivoPesoSerializer, ProgresoImcSerializer


class ProgresoImcViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProgresoImcSerializer

    def get_queryset(self):
        queryset = ProgresoImc.objects.filter(
            usuario=self.request.user.detalles)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['usuario'] = request.user.detalles.pk
        return super().create(request, *args, **kwargs)


class ObjetivoPesoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ObjetivoPesoSerializer

    def get_queryset(self):
        queryset = ObjetivoPeso.objects.filter(
            usuario=self.request.user.detalles)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['usuario'] = request.user.detalles.pk
        return super().create(request, *args, **kwargs)
