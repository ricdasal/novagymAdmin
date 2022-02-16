from django.urls import path
from .views import *
from .apps import SeguridadConfig

app_name = SeguridadConfig.name
urlpatterns = [
    path("login/", login_user, name="login_admin"),
    path("logout/", logout_user, name="logout_admin"),

    path('usuarios/', ListarUsuarios.as_view(), name='listar'),
    path('usuarios/agregar/', CrearUsuario.as_view(), name='agregar'),
    path('usuarios/editar/<pk>/', EditarUsuario.as_view(), name='editar'),
    path('usuarios/eliminar/<pk>/', usuario_confirmar_eliminacion,
         name='eliminar'),
    path('usuarios/activar/<pk>/', usuario_confirmar_activar,
         name='activar'),

]
