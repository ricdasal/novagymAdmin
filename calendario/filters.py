import django_filters
from calendario.forms import HorarioHorarioFilterForm, HorarioMaquinaFilterForm, HorarioReservaFilterForm, MaquinaFilterForm, MaquinaReservaFilterForm
from django_filters.widgets import RangeWidget
from gimnasio.models import Gimnasio
from seguridad.models import UserDetails
from .models import Horario, HorarioHorario, HorarioReserva,Maquina, MaquinaReserva, Zona
class CalendarioFilter(django_filters.FilterSet):
    class Meta:
        model = Horario
        fields = ['gimnasio',
                  ]

class MaquinaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains", label='Nombre')
    categoria = django_filters.ChoiceFilter(choices=Maquina.Categoria.choices)
    reservable = django_filters.ChoiceFilter(choices=(('1', 'Reservable'), ('0', 'No reservable')))
    activo = django_filters.ChoiceFilter(choices=(('1', 'Activo'), ('0', 'Inactivo')))
    gimnasio = django_filters.ModelChoiceFilter(queryset=Gimnasio.objects.all())
    zona = django_filters.ModelChoiceFilter(queryset=Zona.objects.all().filter(tipo="maquinas"))
    class Meta:
        model = Maquina
        fields = ['nombre',
                  'categoria',
                    'reservable',
                    'activo',
                  'gimnasio',
                  'zona'
                  ]
        form = MaquinaFilterForm

class MaquinaReservaFilter(django_filters.FilterSet):
    maquina = django_filters.ModelChoiceFilter(queryset=Maquina.objects.all())
    usuario = django_filters.CharFilter(field_name='usuario__cedula',lookup_expr="exact", label='Nº de cédula')
    fecha= django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}))
    class Meta:
        model = MaquinaReserva
        fields = ['usuario',
                  'maquina',
                  'fecha'
                  ]
        form = MaquinaReservaFilterForm

class HorarioReservaFilter(django_filters.FilterSet):
    horario = django_filters.ModelChoiceFilter(queryset=Horario.objects.all())
    usuario = django_filters.CharFilter(field_name='usuario__cedula',lookup_expr="exact", label='Nº de cédula')
    fecha= django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}))
    class Meta:
        model = HorarioReserva
        fields = ['usuario',
                  'horario',
                  'fecha'
                  ]
        form = HorarioReservaFilterForm

class HorarioHorarioFilter(django_filters.FilterSet):
    horario = django_filters.ModelChoiceFilter(field_name='horario',queryset=Horario.objects.all(),label='Actividad')
    class Meta:
        model = HorarioHorario
        fields = ['dia',
                  'horario'
                  ]
        form = HorarioHorarioFilterForm

class HorarioMaquinaFilter(django_filters.FilterSet):
    maquina = django_filters.ModelChoiceFilter(field_name='maquina',queryset=Maquina.objects.all(),label='Máquina')
    class Meta:
        model = HorarioHorario
        fields = ['dia',
                  'maquina'
                  ]
        form = HorarioMaquinaFilterForm