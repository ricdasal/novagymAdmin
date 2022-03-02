import django_filters
from django.contrib.auth.models import Group
from django.db.models import Q
from django.db.models.aggregates import Sum
from django_filters.widgets import RangeWidget

from seguridad.forms import UsuarioFilterForm
from seguridad.models import UserDetails


class UsuarioFilter(django_filters.FilterSet):
    usuario__email = django_filters.CharFilter(lookup_expr="icontains")
    fecha_nacimiento = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}))
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}))
    rol = django_filters.ModelChoiceFilter(
        queryset=Group.objects.all(), field_name='usuario__groups')

    class Meta:
        model = UserDetails
        fields = ['usuario__email',
                  'cedula',
                  'nombres',
                  'apellidos',
                  'fecha_nacimiento',
                  "sexo",
                  "rol",
                  "created_at",
                  ]
        form = UsuarioFilterForm
