from django.contrib import admin

from notificaciones.models import Notificacion, NotificacionUsuario

# Register your models here.
admin.site.register(Notificacion)
admin.site.register(NotificacionUsuario)
