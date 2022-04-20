import django_filters
from calendario.models import Maquina,MaquinaReserva,PosicionMaquina,Horario,HorarioReserva,Posicion

""" class MaquinaFilter(django_filters.FilterSet):
    class Meta:
        model = Maquina
        fields = ['nombre',
                  'categoria',
                    'reservable',
                    'activo',
                  'gimnasio',
                  'zona'
                  ] """