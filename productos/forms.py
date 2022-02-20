from crispy_forms.helper import FormHelper
from django import forms
from .models import *
from crispy_forms.layout import Column, Div, Field, Layout, Row
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        
        labels = {
            "imagen": "Imagen de referencia"
        }
        widgets = {
            "imagen": forms.ClearableFileInput(),
        }
        fields = ('nombre','imagen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('codigo','nombre', 'descripcion','precio_referencial','imagen','categoria', 'valor_presentacion','talla','unidad_presentacion')

        valor_presentacion=forms.DecimalField(min_value=0),
        precio_referencial=forms.DecimalField(min_value=0)
        labels = {
            "imagen": "Imagen del producto"
        }
        widgets = {
            "imagen": forms.ClearableFileInput(),
            "descripcion":forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('codigo', css_class='col-6'),
                Column('nombre', css_class='col-6'),
                Column('descripcion', css_class='col-6'),
                Column('categoria', css_class='col-6'),
                Column('talla', css_class='col-6'),
            ),
            Row(
                Column('valor_presentacion', css_class='col-6'),
                Column('unidad_presentacion', css_class='col-6'),
                Column('precio_referencial', css_class='col-6'),
            ),
        )


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario  

        precio=forms.DecimalField(min_value=0)

        fields = ('precio','stock')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('precio', css_class='col-6')
            ),
            Row(
                Column('stock', css_class='col-6')
            )
        )

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = ProductoDescuento
        fields = ('porcentaje_descuento', 'producto', 'fecha_hora_desde','fecha_hora_hasta','estado')
        widgets={
            "fecha_inicio": forms.SelectDateWidget(attrs={'style': 'display: inline-block; width: 33%;'}),
            "fecha_fin": forms.SelectDateWidget(attrs={'style': 'display: inline-block; width: 33%;'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False

ProductoMeta=forms.inlineformset_factory(Producto,Inventario,InventarioForm,extra=1,can_delete=False)