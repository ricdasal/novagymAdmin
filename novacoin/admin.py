from django.contrib import admin

from novacoin.models import (Cartera, DetalleCartera, MotivoCanje,
                             RangoCambioCoins)

# Register your models here.
admin.site.register(Cartera)
admin.site.register(MotivoCanje)
admin.site.register(DetalleCartera)
admin.site.register(RangoCambioCoins)
