from rest_framework import permissions, viewsets

from novagym.models import ProgresoImc
from novagym.serializers import ProgresoImcSerializer


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
