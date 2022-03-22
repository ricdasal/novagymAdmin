import django_filters

from productos.forms import ProductoFilterForm
from .models import Producto,Categoria

class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains", label='Nombre')
    categoria = django_filters.ModelChoiceFilter(queryset=Categoria.objects.all())
    talla = django_filters.ChoiceFilter(choices=Producto.Talla.choices)
    usaNovacoins = django_filters.ChoiceFilter(choices=(('1', 'En Novacoins'), ('0', 'En dólares')),label='Forma de pago')
    class Meta:
        model = Producto
        fields = ['nombre',
                  'categoria',
                  'talla',
                  'usaNovacoins'
                  ]
        form = ProductoFilterForm

class CategoriaFilter(django_filters.FilterSet):
    class Meta:
        model = Categoria
        fields = ['id',
                  'nombre'
                  ]