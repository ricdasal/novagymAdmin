from django.urls import path
from .views import *
from .apps import ReportesConfig

app_name = ReportesConfig.name

urlpatterns = [
    path('listarDolares/', ListarTransaccionDolares.as_view(), name='listarDolares'),
    path('listarCoins/', ListarTransaccionCoins.as_view(), name='listarCoins'),
    path('verProductos/<int:id>/', verProductos, name='verProductos'),
]