from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(ObjetivoPeso)
admin.site.register(ProgresoImc)
admin.site.register(Transaccion)
admin.site.register(TipoPago)
admin.site.register(DetalleTransaccionMembresia)
admin.site.register(DetalleTransaccionProducto)
