from django.urls import path

from calendario.views import ReservarMaquina
from .views import *
from .apps import ReservasConfig

app_name = ReservasConfig.name

urlpatterns = [
     path('listarMaquinas/', ListarMaquinas.as_view(), name='listarMaquinas'),
     path('crearMaquina/',CrearMaquina.as_view(),name="crearMaquina"),
     path('editarMaquina/<int:pk>',UpdateMaquina.as_view(),name="editarMaquina"),
     path('reservasMaquinas/', ListarReservasMaquinas.as_view(), name='reservasMaquinas'),
     path('listarHorarios/', ListarReservasHorarios.as_view(), name='listarHorarios'),
     path('eliminarMaquina/<int:id>',deleteMaquina,name="eliminarMaquina"),
     path('change/<int:pk>',ChangeState,name="change"),
     path('reservable/<int:pk>',changeReservable,name="reservable"),
]