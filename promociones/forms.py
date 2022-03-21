from crispy_forms.helper import FormHelper
from django import forms
from .models import *
from crispy_forms.layout import Column, Div, Field, Layout, Row
from .widgets import DatePickerInput, DateTimePickerInput

class PromocionesForm(forms.ModelForm):
    class Meta:
        model= Promociones
        labels = {
            "imagen": "Logo del sponsor",
            "descripcion": "descripcion"
        }
        fields = ('titulo', 'fecha_hora_inicio', 'fecha_hora_fin', 'imagen', 'categoria','membresia','descuento_categoria','descuento_membresia')

        widgets = {
            "fecha_hora_inicio": DateTimePickerInput(),
            "fecha_hora_fin": DateTimePickerInput(),
            "descuento_categoria":forms.NumberInput(attrs={'min':0,'max': 100}),
            "descuento_membresia":forms.NumberInput(attrs={'min':0,'max': 100}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('titulo', css_class='col-6'),
                Column('activo', css_class='col-6'),
                Column('categoria', css_class='col-6'),
                Column('membresia', css_class='col-6'),
            ),
            Row(
                Column('descuento_categoria', css_class='col-6'),
                Column('descuento_membresia', css_class='col-6'),
                Column('fecha_hora_inicio', css_class='col-6'),
                Column('fecha_hora_fin', css_class='col-6'),
                Column('imagen', css_class='col-6'),
                
            ),
        )