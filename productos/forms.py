from crispy_forms.helper import FormHelper
from django import forms
from .models import *

""" class SponsorForm(forms.ModelForm):
    class Meta:
        model:Sponsor
        labels = {
            "imagen": "Logo del sponsor"
        }
        widgets = {
            "imagen": forms.ClearableFileInput(),
        }
        fields = ('nombre', 'descripcion', 'telefono', 'nombre_contacto', 'url','imagen')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False """

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

        labels = {
            "imagen": "Imagen del producto"
        }
        widgets = {
            "imagen": forms.ClearableFileInput(),
        }
        fields = ('codigo','nombre', 'descripcion','precio_referencial','imagen','categoria', 'valor_presentacion','talla','unidad_presentacion')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ('precio','producto','stock')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = ProductoDescuento
        fields = ('producto','porcentaje_descuento', 'fecha_hora_desde','fecha_hora_hasta','estado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False