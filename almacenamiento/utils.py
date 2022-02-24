from decimal import Decimal
from .models import *

def tamanio_archivos(archivos):
   tamanio = 0
   for archivo in archivos:
      tamanio += archivo['almacenamiento_utilizado']
   return tamanio

def almacenamiento_disponible_user(user, archivos):
   almacenamiento = AlmacenamientoUsuario.objects.get(usuario=user)
   if almacenamiento.asignado == -1: #-1 significa que no hay un limite de almacenamiento
      return True

   tamanio = tamanio_archivos(archivos)   
   if (Decimal(tamanio) + almacenamiento.usado) > (almacenamiento.asignado + almacenamiento.comprado):
      return False
   return True

def almacenamiento_disponible_servidor(archivos):
   almacenamiento = AlmacenamientoGlobal.objects.get(id=1)
   if almacenamiento.capacidad_max == -1 and almacenamiento.servidor == -1:
      return True
   tamanio = tamanio_archivos(archivos)
   almacenamiento_actual = Decimal(tamanio) + almacenamiento.total_usado
   if almacenamiento_actual > almacenamiento.servidor:
      return False
   elif Decimal(tamanio) > almacenamiento.capacidad_max:
      return False
   return True
   
