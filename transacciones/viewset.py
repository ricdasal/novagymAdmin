from rest_framework import permissions, viewsets
from .models import Transaccion, DetalleTransaccion
from .serializers import TransaccionSerializer

class TransaccionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = TransaccionSerializer

    def get_queryset(self):
        queryset = Transaccion.objects.filter(usuario=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['usuario'] = request.user.pk
        return super().create(request, *args, **kwargs)
