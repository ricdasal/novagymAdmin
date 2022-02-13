from django.urls import path, include
from .views import *
from .apps import NovagymConfig

app_name = NovagymConfig.name

urlpatterns = [
    path('', home, name='principal'),
]
