from django.urls import path
from .views import *
from .apps import GimnasioConfig

app_name = GimnasioConfig.name

urlpatterns = [
     #Gimnasio-Contacto
     path('create/',createGimnasio,name='createGimnasio'),
     path('gimnasio-list/', gimnasioList, name='gimnasio-overview'),
     path('gimnasio-detail/<str:id>', gimnasioDetail, name='gimnasio-detail'),
     path('gimnasio-create/', gimnasioCreate, name='gimnasio-create'),
     path('gimnasio-update/<str:id>', gimnasioUpdate, name='gimnasio-update'),
     path('gimnasio-delete/<str:id>', gimnasioDelete, name='gimnasio-delete'),

]