from django.urls import path
from .views import *
from .apps import ChartsConfig

app_name = ChartsConfig.name


urlpatterns = [
    path("listar/",listar,name="reportes"),
    path("listarNc/",listarNc,name="reportesNc"),
    path('productos/', productos_chart, name='productos'),
    path('stockChart/<int:id>', grafico_categorias, name='stockChart'),
    path('dateChart/<fechaI>&<fechaF>', grafico_fechas, name='dateChart'),
]
