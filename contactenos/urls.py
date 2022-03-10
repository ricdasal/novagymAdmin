from django.urls import path
from .views import *
from .apps import ContactenosConfig

app_name = ContactenosConfig.name

urlpatterns = [
     #Gimnasio-Contacto
     
    path('', contact, name='contact'),
    path('sendEmail/', sendEmail, name='sendEmail'),
    path('buzon/', ShowBuzon.as_view(), name='buzon'),
    path('markAsRead/<int:id>', markAsRead, name='markAsRead'),
    path('eliminar/<int:id>', deleteMail, name='eliminar'),
    path('leer/<int:id>', readMail, name='leer')
]