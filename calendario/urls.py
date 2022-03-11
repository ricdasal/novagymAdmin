from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from calendario.views import *


urlpatterns = [
    path('',ShowCalendario.as_view(),name="calendario")
]