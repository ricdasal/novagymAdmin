from django.urls import path
from .views import *
from .apps import AfiliadosConfig

app_name = AfiliadosConfig.name


urlpatterns = [
     path('entregar/', entregarNovacoins, name='entregar'),
]