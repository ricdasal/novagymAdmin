from django.urls import path
from .views import *
from .apps import PromocionesConfig

app_name = PromocionesConfig.name

urlpatterns = [
     path('listar/', ListarPromociones.as_view(), name='listar'),
     path('crear/', CrearPromociones.as_view(), name='crear'),
     path('editar/<int:pk>/', UpdatePromocion.as_view(), name='editar'),
     path('eliminar/<int:id>/', deletePromocion, name='eliminar'),
     path('changeState/<int:pk>/', ChangeState, name='changeState'),
     path('getPromociones/', getPromociones.as_view(), name='getPromociones'),
]