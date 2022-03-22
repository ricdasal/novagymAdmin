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
        fields = ('nombre','imagen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('codigo','nombre', 'descripcion','precio_referencial','imagen','categoria', 'valor_presentacion','talla','unidad_presentacion','usaNovacoins')

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
            Row(
                Column('usaNovacoins', css_class='col-6'),
                Column('imagen', css_class='col-6'),
            ),
        )


class InventarioForm(forms.ModelForm):
    class Meta:
        fields = ('precio','novacoins','stock')
        model = Inventario  

        precio=forms.DecimalField(min_value=0)
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('precio', css_class='col-6'),
                Column('novacoins', css_class='col-6')
            ),
            Row(
                Column('stock', css_class='col-6')
            )
        )

""" class InventarioFormNC(forms.ModelForm):
    class Meta:
        model = Inventario  
        fields = ('novacoins','stock')

        widgets = {
            "usaNovacoins":forms.CheckboxInput(attrs={'checked':True})
        }
        novacoins=forms.IntegerField(min_value=0)
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('novacoins', css_class='col-6'),
            ),
            Row(
                Column('stock', css_class='col-6')
            )
        ) """

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = ProductoDescuento
        
        fields = ('porcentaje_descuento', 'fecha_hora_desde','fecha_hora_hasta','estado')
        labels = {
            "estado": "Descuento activo",
            'porcentaje_descuento':"Valor de descuento (Sin descuento: 0)"
        }
        
        widgets={
            "porcentaje_descuento":forms.NumberInput(attrs={'min':0,'max': 100}),
            "fecha_hora_hasta": DateTimePickerInput(),
            "fecha_hora_desde": DateTimePickerInput(),
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
                Column('usaNovacoins', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
            ),
            Row(
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )

ProductoMeta=forms.inlineformset_factory(Producto,Inventario,InventarioForm,extra=1,can_delete=False)
DescuentoMeta=forms.inlineformset_factory(Producto,ProductoDescuento,DescuentoForm,extra=1,can_delete=False)

ProductoMetaU=forms.inlineformset_factory(Producto,Inventario,InventarioForm,extra=0,can_delete=False)
DescuentoMetaU=forms.inlineformset_factory(Producto,ProductoDescuento,DescuentoForm,extra=0,can_delete=False)