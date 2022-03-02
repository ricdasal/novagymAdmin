from django.urls import path, re_path

from .apps import SeguridadConfig
from .views import *

app_name = SeguridadConfig.name
urlpatterns = [
    path("login/", login_user, name="login_admin"),
    path("logout/", logout_user, name="logout_admin"),

    re_path(r'^usuarios/(?P<type>\w{1})/$',
            ListarUsuarios.as_view(), name='listar'),
    path('usuarios/agregar/', CrearUsuario.as_view(), name='agregar'),
    path('usuarios/editar/<int:pk>/', EditarUsuario.as_view(), name='editar'),
    path('usuarios/eliminar/<int:pk>/', usuario_confirmar_eliminacion,
         name='eliminar'),
    path('usuarios/activar/<int:pk>/', usuario_confirmar_activar,
         name='activar'),
    re_path(r'^usuarios/rol/detalles/(?:(?P<pk>\d+)?)$',
            rol_permisos_template, name='ver_rol'),
    path('usuarios/rol/agregar/', CrearRolUsuario.as_view(), name='agregar_rol'),
    re_path(r'^usuarios/rol/editar/(?:(?P<pk>\d+)?)$',
            EditarRolUsuario.as_view(), name='editar_rol'),
    path('usuarios/rol/eliminar/<pk>/',
         rol_confirmar_eliminacion, name='eliminar_rol'),
]
