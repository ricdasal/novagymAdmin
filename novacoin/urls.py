from django.urls import path

from .apps import NovacoinConfig
from .views import *

app_name = NovacoinConfig.name
urlpatterns = [
    path('', ListarRecompensas.as_view(), name='listar'),
    path('agregar/', CrearRecompensa.as_view(), name='agregar'),
    path('editar/<int:pk>/', EditarRecompensa.as_view(), name='editar'),
    path('eliminar-perma/<int:pk>/', deleteRecompensa, name='eliminar_perma'),
    path('change/<int:pk>/', changeState, name='cambiar_estado'),
    path('tasa/<int:pk>/', EditarTasaCambio.as_view(), name='tasa'),
]
