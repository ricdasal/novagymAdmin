from django.urls import path
from .views import ListarTransaccion, AnularTransaccion, showDetalleTransaccion, PaymentezRefound
from .apps import TransaccionesConfig


app_name = TransaccionesConfig.name

urlpatterns = [
    path('listar/', ListarTransaccion.as_view(), name='listar'),
    path('anular/<int:id>', AnularTransaccion, name='anular'),
    path('detalles/<int:id>', showDetalleTransaccion, name='detalles'),
    path('refound/<int:id>', PaymentezRefound, name='refound')
]