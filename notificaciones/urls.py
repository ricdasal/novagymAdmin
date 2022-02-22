from django.urls import path
from .views import *
from .apps import NotificacionesConfig

app_name = NotificacionesConfig.name

urlpatterns = [
     path('listar/', ListarNotificacion.as_view(), name='listar'),
     path('notificacion-list/', notificacionList, name='notificacion-list'),
     path('notificacion-detail/<str:id>', notificacionDetail, name='notificacion-detail'),
     path('notificacion-create/', notificacionCreate, name='notificacion-create'),
     path('notificacion-update/<str:id>', notificacionUpdate, name='notificacion-update'),
     path('notificacion-delete/<str:id>', notificacionDelete, name='notificacion-delete'),
     path('deleteNotificacion/<int:pk>/', deleteNotificacion, name='deleteNotificacion'),
     path('crear/', CrearNotificacion.as_view(), name='crear'),
     path('editar/<str:pk>', UpdateNotificacion.as_view(), name='update'),
]