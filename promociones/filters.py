import django_filters
from .models import Promociones
class PromocionesFilter(django_filters.FilterSet):
    class Meta:
        model = Promociones
        fields = ['id',
                  'titulo',
                  'categoria',
                  'membresia',
                  'activo'
                  ]