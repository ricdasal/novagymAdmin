import os
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from datetime import datetime, timedelta
from comunidad.models import Historia

def eliminar_historias():
    historias = list(Historia.objects.all())
    for historia in historias:
        fecha_creacion = historia.fecha_creacion  #2022-03-18 20:59:40.219319+00:00
        hoy = datetime.now(fecha_creacion.tzinfo) ##2022-03-18 23:59:59.219319+00:00
        delta = timedelta(days=1)                 #1 day, 0:00:00
        diferencia = hoy - fecha_creacion
        if (diferencia > delta ):
            if historia.archivo:
                historia.reducir_almacenamiento()
            historia.delete()

eliminar_historias()