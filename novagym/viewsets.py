from rest_framework import permissions, viewsets

from novagym.models import DetalleTransaccionMembresia, DetalleTransaccionProducto, ObjetivoPeso, ProgresoImc, Transaccion
from novagym.serializers import DetalleTransaccionMembresiaSerializer, DetalleTransaccionProductoSerializer, ObjetivoPesoSerializer, ProgresoImcSerializer, TransaccionMembresiaSerializer, TransaccionProductoSerializer


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


class TransaccionMembresiaViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = TransaccionMembresiaSerializer

    def get_queryset(self):
        queryset = Transaccion.objects.filter(
            usuario=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['usuario'] = request.user.pk
        return super().create(request, *args, **kwargs)


class TransaccionProductoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = TransaccionProductoSerializer

    def get_queryset(self):
        queryset = Transaccion.objects.filter(
            usuario=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['usuario'] = request.user.pk
        return super().create(request, *args, **kwargs)
