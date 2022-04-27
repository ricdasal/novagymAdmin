from django.urls import path
from .views import *
from .apps import AfiliadosConfig

app_name = AfiliadosConfig.name


urlpatterns = [
     #path('listar/', ListarSponsors.as_view(), name='listar'),

]