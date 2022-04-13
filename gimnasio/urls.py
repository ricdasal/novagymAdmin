from django.urls import path
from .views import *
from .apps import GimnasioConfig

app_name = GimnasioConfig.name

urlpatterns = [
     #Gimnasio-Contacto
     path('changeState/<int:pk>',changeState,name='changeState'),
     path('update/<int:pk>',UpdateGimnasio.as_view(),name='update'),
     path('changeAforo/',changeAforo,name='changeAforo'),
     path('listar/',ListarGimnasio.as_view(),name='listar'),
     path('crear/',CrearGimnasio.as_view(),name='crear'),
     path('eliminar/<int:id>',deleteGimnasio,name='eliminar'),
     path('getGimnasios/', GetGimnasios.as_view(), name='getGimnasios'),
     path('getGimnasios/<int:opc>', GetGimnasios.as_view(), name='getGimnasios'),
]