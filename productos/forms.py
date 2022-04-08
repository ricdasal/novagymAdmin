from cProfile import label
import datetime
from crispy_forms.helper import FormHelper
from django import forms
from .models import *
from crispy_forms.layout import Column, Div, Field, Layout, Row
from .widgets import DateTimePickerInput
from crispy_forms.bootstrap import StrictButton


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria

        labels = {
            "imagen": "Imagen de referencia"
        }
        widgets = {
            "imagen": forms.ClearableFileInput(),
        }
        fields = ('nombre', 'imagen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('presentacion', 'nombre', 'descripcion',
                  'imagen', 'categoria', 'talla', 'usaNovacoins')

        valor_presentacion = forms.DecimalField(min_value=0),
        precio_referencial = forms.DecimalField(min_value=0)
        labels = {
            "usaNovacoins": "Este producto se adquiere con Novacoins",
            "imagen": "Imagen del producto",
            "presentacion": "Presentación del producto"
        }
        widgets = {
            "imagen": forms.ClearableFileInput(),
            "descripcion": forms.Textarea(attrs={'rows': 4, 'cols': 15,'maxlength': '130'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-6'),
                Column('presentacion', css_class='col-6'),
                Column('descripcion', css_class='col-6'),
                Column('categoria', css_class='col-6'),
                Column('talla', css_class='col-6'),
            ),
            Row(
                Column('imagen', css_class='col-6'),
            ),
            Row(
                Column('usaNovacoins', css_class='col-6'),            ),
        )


class InventarioForm(forms.ModelForm):
    class Meta:
        fields = ('precio', 'precioCompra', 'novacoins', 'stock')
        model = Inventario
        labels={
            "precioCompra": "Precio de compra",
            "precio": "Precio de venta (PVP en $)",
            "novacoins":"Precio en Novacoins (NC)"
        }
        precio = forms.DecimalField(min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('precio', css_class='col-6'),
                Column('novacoins', css_class='col-6'),
                Column('precioCompra', css_class='col-6'),
            ),
            Row(
                Column('stock', css_class='col-6')
            )
        )

    def clean(self):
        cleaned_data = super(InventarioForm, self).clean()
        precio = cleaned_data.get("precio")
        precioCompra = cleaned_data.get("precioCompra")
        if precio and precioCompra:
            if precio < precioCompra:
                raise forms.ValidationError(
                    "El precio de venta no puede ser menor al de compra")
        return cleaned_data


class DescuentoForm(forms.ModelForm):
    class Meta:
        model = ProductoDescuento

        fields = ('porcentaje_descuento', 'fecha_hora_desde',
                  'fecha_hora_hasta', 'estado')
        labels = {
            "estado": "Descuento activo",
            'porcentaje_descuento': "Porcentaje(%) de descuento (Sin descuento: 0)"
        }

        widgets = {
            "porcentaje_descuento": forms.NumberInput(attrs={'min': 0, 'max': 100}),

            "fecha_hora_desde": forms.DateTimeInput(
                format=('%Y-%m-%dT%H:%M'),
                attrs={'class': 'form-control',
                       'type': 'datetime-local'
                       }),

            "fecha_hora_hasta": forms.DateTimeInput(
                format=('%Y-%m-%dT%H:%M'),
                attrs={'class': 'form-control',
                       'type': 'datetime-local'
                       }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('porcentaje_descuento', css_class='col-6'),
                Column('estado', css_class='col-6')
            ),
            Row(
                Column('fecha_hora_desde', css_class='col-6'),
                Column('fecha_hora_hasta', css_class='col-6')
            )
        )

    def clean(self):
        cleaned_data = super(DescuentoForm, self).clean()
        fecha_hora_desde = cleaned_data.get("fecha_hora_desde")
        fecha_hora_hasta = cleaned_data.get("fecha_hora_hasta")
        if fecha_hora_desde and fecha_hora_hasta:
            if fecha_hora_hasta < fecha_hora_desde:
                raise forms.ValidationError(
                    "La fecha de fin no puede ser anterior a la fecha de inicio.")
            elif fecha_hora_desde.replace(tzinfo=None) < (datetime.datetime.today() - datetime.timedelta(days=1)):
                raise forms.ValidationError(
                    "La fecha de inicio no puede ser anterior a la fecha actual.")
        return cleaned_data


class ProductoFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('categoria', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
            ),
            Row(
                Column('talla', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('usaNovacoins',
                       css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
            ),
            Row(
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )


ProductoMeta = forms.inlineformset_factory(
    Producto, Inventario, InventarioForm, extra=1, can_delete=False)
DescuentoMeta = forms.inlineformset_factory(
    Producto, ProductoDescuento, DescuentoForm, extra=1, can_delete=False)

ProductoMetaU = forms.inlineformset_factory(
    Producto, Inventario, InventarioForm, extra=0, can_delete=False)
DescuentoMetaU = forms.inlineformset_factory(
    Producto, ProductoDescuento, DescuentoForm, extra=0, can_delete=False)
