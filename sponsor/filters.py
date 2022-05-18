import django_filters

from sponsor.forms import SucursalFilterForm
from .models import Sponsor, Sucursal
class SponsorFilter(django_filters.FilterSet):
    class Meta:
        model = Sponsor
        fields = ['id',
                  'codigo',
                  'nombre',
                  'descripcion',
                  'telefono',
                  "nombre_contacto",
                  'url',
                  'fecha_inicio',
                  'fecha_fin',
                  'activo',
                  ]

class SucursalFilter(django_filters.FilterSet):
    nombre=django_filters.CharFilter(field_name='nombre',lookup_expr="icontains", label='Nombre')
    activo=django_filters.ChoiceFilter(choices=(('1', 'Activo'), ('0', 'Inactivo')))
    class Meta:
        model = Sucursal
        fields = ['activo',
                  'nombre',
                  'sponsor',
                  ]
        form = SucursalFilterForm