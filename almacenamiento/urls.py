from django.urls import path
from .views import *
from .apps import AlmacenamientoConfig

app_name = AlmacenamientoConfig.name

urlpatterns = [
    path('almacenamiento_usuario/', AlmacenamientoUsuarioView.as_view(), name='almacenamiento_usuario'),

    path('configurar_almacenamiento/', configurar_almacenamiento, name='configurar_almacenamiento'),

    path('configurar_usuario/<int:user>/', configurar_usuario, name='configurar_usuario'),

    path('administrar_excepciones/', AdministrarExcepcionesView.as_view(), name='administrar_excepciones'),

    path('modificar_almacenamiento_usuario/<int:user>/<str:page>/', modificar_almacenamiento_usuario, name='modificar_almacenamiento_usuario'),
]
