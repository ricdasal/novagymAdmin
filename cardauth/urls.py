from django.urls import path
from .views import *

urlpatterns = [
    #añade cvc de tarjeta
    path('tarjeta/add/', addCodigoAuth),

    #busca el cvc de la tarjeta segun el token
    path('tarjeta/del/', delCodigoAuth),

    #borra el cvc de la tarjeta segun el token 
    path('tarjeta/', getCodigoAuth)
]