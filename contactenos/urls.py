from django.urls import path
from .views import *
from .apps import ContactenosConfig

app_name = ContactenosConfig.name

urlpatterns = [
     #Gimnasio-Contacto
     
    path('', contact, name='contact'),
    path('demo/', sendEmail, name='demo')

]