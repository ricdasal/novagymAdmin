import django_filters
from calendario.forms import MaquinaFilterForm, MaquinaReservaFilterForm
from calendario.models import Maquina, MaquinaReserva

from gimnasio.models import Gimnasio
from seguridad.models import UserDetails

class MaquinaReservaFilter(django_filters.FilterSet):
    maquina = django_filters.ModelChoiceFilter(queryset=Maquina.objects.all())
    usuario = django_filters.ModelChoiceFilter(queryset=UserDetails.objects.all())
    fecha= django_filters.DateFromToRangeFilter()
    class Meta:
        model = MaquinaReserva
        fields = ['usuario',
                  'maquina',
                  'fecha'
                  ]
        form = MaquinaReservaFilterForm