import django_filters
from .models import Horario,Maquina
class CalendarioFilter(django_filters.FilterSet):
    class Meta:
        model = Horario
        fields = ['gimnasio',
                  ]

class MaquinaFilter(django_filters.FilterSet):
    class Meta:
        model = Maquina
        fields = ['id',
                  ]