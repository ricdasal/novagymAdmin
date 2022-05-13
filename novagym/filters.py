import django_filters
from calendario.forms import HorarioReservaFilterForm, MaquinaFilterForm, MaquinaReservaFilterForm
from django_filters.widgets import RangeWidget
from gimnasio.models import Gimnasio
from novagym.forms import TransaccionDolaresFilterForm
from seguridad.models import UserDetails
from .models import Transaccion

class TransaccionDolaresFilter(django_filters.FilterSet):
    usuario = django_filters.CharFilter(field_name='usuario__userdetails__cedula',lookup_expr="exact", label='Nº de cédula')
    created_at= django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}),label="Fecha de creación")
    class Meta:
        model = Transaccion
        fields = ['estado',
                  'created_at',
                  'usuario',
                  ]
        form = TransaccionDolaresFilterForm