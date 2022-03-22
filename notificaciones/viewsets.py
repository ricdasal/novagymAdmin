from django.db.models import Q
from rest_framework import permissions, viewsets

from notificaciones.models import NotificacionUsuario
from notificaciones.serializers import NotificacionUsuarioSerializer


class NotificacionUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionUsuarioSerializer
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = NotificacionUsuario.objects.filter(
            Q(receiver=self.request.user) | Q(grupo_usuarios__name="Todos"))
        return queryset
