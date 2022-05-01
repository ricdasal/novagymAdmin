from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from push_notifications.models import GCMDevice
from notificaciones.models import Notificacion
from django.db.models import Q

class Command(BaseCommand):
    help = 'Envío de notificaciones automáticas programadas'

    def handle(self, *args, **options):
        try:
            domain = "https://devsnovagym.pythonanywhere.com"
            current_date = timezone.now()
            notifaciones = Notificacion.objects.filter(Q(tipo = Notificacion.Tipo.Admin)&Q(frecuencia=Notificacion.Frecuencia.D1))
            for notif in notifaciones:
              if current_date.date() >= notif.fecha_inicio and current_date.date() <=notif.fecha_fin and current_date.time() <= notif.hora:
                  data = {
                    "imagen":domain+notif.imagen.url,
                    'id':str(notif.id),
                  }
                  GCMDevice.objects.all().send_message(
                    notif.cuerpo, extra=data)
        except Exception as e:
            raise CommandError('Ha ocurrido un error al enviar las notificaciones: '+e.__str__())

        self.stdout.write(self.style.SUCCESS('Operación realizada correctamente'))