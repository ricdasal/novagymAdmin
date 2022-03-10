from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from calendario.views import *

from comunidad.urls import comunidad_api

urlpatterns = [
    path('',ShowCalendario.as_view(),name="calendario")
]