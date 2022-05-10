from django.urls import path
from knox import views as knox_views
from membresia.viewsets import (BeneficioViewSet, DescuentoViewSet,
                                HistorialMemebresiaViewset, MembresiaViewSet)
from notificaciones.viewsets import NotificacionUsuarioViewSet
from novagym.viewsets import (ObjetivoPesoViewSet, ProgresoImcViewSet,
                              TransaccionMembresiaViewset,
                              TransaccionProductoViewSet)
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet
from rest_framework import routers
from seguridad.viewsets import (ChangePasswordView, DetallesViewSet, LoginAPI,
                                RegistrarAPI)

"""
 APIS Gym
"""
novagym = routers.DefaultRouter()
novagym.register('usuarios', DetallesViewSet, 'usuario')
novagym.register('objetivo-peso', ObjetivoPesoViewSet, 'imc')
novagym.register('imc', ProgresoImcViewSet, 'imc')
novagym.register('membresias', MembresiaViewSet, 'membresia')
novagym.register('membresias-usuario',
                 HistorialMemebresiaViewset, 'membresias-usuario')
novagym.register('descuentos', DescuentoViewSet, 'descuento')
novagym.register('beneficios', BeneficioViewSet, 'beneficio')
novagym.register(r'registrar/gcm', GCMDeviceAuthorizedViewSet)
novagym.register('notificacion-usuario',
                 NotificacionUsuarioViewSet, 'notificacion-usuario')
novagym.register('transaccion-producto',
                 TransaccionProductoViewSet, 'transaccion-producto')
novagym.register('transaccion-membresia',
                 TransaccionMembresiaViewset, 'transaccion-membresia')
novagym_api = novagym.urls

"""
 APIS Seguridad
"""
seguridad_api = [
    path('registrarse/', RegistrarAPI.as_view(), name='regitrarse'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(),
         name='logoutall'),
    path('cambiar-password/', ChangePasswordView.as_view(), name='cambiar-password'),
]
