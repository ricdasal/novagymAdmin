from crispy_forms.helper import FormHelper
from django import forms
from .models import *
from crispy_forms.layout import Column, Div, Field, Layout, Row
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

class GimnasioForm(forms.ModelForm):
    class Meta:
        model = Gimnasio
        labels = {
            "imagen": "Imagen de referencia",
            "estado": "Gimnasio activo"
        }
        widgets = {
            "imagen": forms.ClearableFileInput(),
            "horario_inicio": TimePickerInput(),
            "horario_fin": TimePickerInput(),
            "aforo": forms.NumberInput(attrs={'min':0,'max': 100})
        }
        fields = ('tipo','nombre', 'imagen','telefono','ubicacion','horario_inicio', 'horario_fin','estado','ciudad','aforo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('tipo', css_class='col-6'),
                Column('nombre', css_class='col-6'),
                Column('ciudad', css_class='col-6'),
                Column('telefono', css_class='col-6'),
                Column('ubicacion', css_class='col-6')
            ),
            Row(
                Column('horario_inicio', css_class='col-6'),
                Column('horario_fin', css_class='col-6'),
                Column('estado', css_class='col-6'),
                Column('aforo', css_class='col-6'),
                Column('imagen', css_class='col-6')
            )
        )
