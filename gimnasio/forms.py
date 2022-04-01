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
            "estado": "Gimnasio activo",
            "aforo": "Aforo (%)",
            "capacidad": "Capacidad de personas",
            "ubicacion":"Dirección"
        }
        widgets = {
            "imagen": forms.ClearableFileInput(),
            "horario_inicio": TimePickerInput(),
            "horario_fin": TimePickerInput(),
            "aforo": forms.NumberInput(attrs={'min':0,'max': 100}),
            "capacidad": forms.NumberInput(attrs={'min':0,'max': 999}),
            "celular": forms.NumberInput(attrs={'type': "tel", "pattern": "^(09)[0-9]{8}"}),
            "telefono": forms.NumberInput(attrs={'type': "tel", "pattern": "^(0)[1-9]{1}(\s){1}[0-9]{7}"})
        }
        fields = ('nombre', 'imagen','telefono','celular','ubicacion','horario_inicio', 'horario_fin','estado','ciudad','aforo','capacidad')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-6'),
                Column('ciudad', css_class='col-6'),
                Column('telefono', css_class='col-6'),
                Column('celular', css_class='col-6'),
                Column('ubicacion', css_class='col-6'),
                Column('estado', css_class='col-6'),
            ),
            Row(
                Column('horario_inicio', css_class='col-6'),
                Column('horario_fin', css_class='col-6'),
                Column('aforo', css_class='col-6'),
                Column('capacidad', css_class='col-6'),
                Column('imagen', css_class='col-6')
            )
        )
    def clean(self):
        cleaned_data = super(GimnasioForm, self).clean()
        horario_inicio = cleaned_data.get("horario_inicio")
        horario_fin = cleaned_data.get("horario_fin")
        if horario_inicio and horario_fin:
            if horario_fin < horario_inicio:
                raise forms.ValidationError("La hora de cierre no puede ser anterior a la hora de apertura.")
        return cleaned_data
