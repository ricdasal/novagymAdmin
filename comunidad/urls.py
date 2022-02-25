from django.urls import path
from .views import *
from .apps import ComunidadConfig

app_name = ComunidadConfig.name

urlpatterns = [
     path('publicacion_reportada/', ListaPublicacionReportada.as_view(), name='publicacion_reportada'),
     path('publicacion_novagym/', ListaPublicacionNovagym.as_view(), name='publicacion_novagym'),

     path('crear-publicacion/', CrearPublicacion.as_view(), name='crear-publicacion'),

     path('aceptar-publicacion/<int:pk>/', aceptar_publicacion, name='aceptar-publicacion'),
     path('eliminar-publicacion/<int:pk>/', CrearPublicacion.as_view(), name='eliminar-publicacion')
]