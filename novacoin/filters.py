import django_filters
from django_filters.widgets import RangeWidget

from novacoin.forms import RangoCambioCoinsFilterForm
from novacoin.models import RangoCambioCoins


class RangoCambioCoinsFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}))
    nombre = django_filters.CharFilter(
        lookup_expr='icontains', field_name='motivo__nombre')

    class Meta:
        model = RangoCambioCoins
        fields = ['created_at', 'nombre']
        form = RangoCambioCoinsFilterForm
