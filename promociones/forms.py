from crispy_forms.helper import FormHelper
from django import forms
from .models import *
from crispy_forms.layout import Column, Div, Field, Layout, Row
from .widgets import DatePickerInput, DateTimePickerInput

class PromocionesForm(forms.ModelForm):
    class Meta:
        model= Promociones
        labels = {
            "imagen": "Banner publicitario",
            "descripcion": "Descripción"
        }
        fields = ('titulo', 'fecha_hora_inicio', 'fecha_hora_fin', 'imagen','correo','descripcion','activo','telefono','celular','nombre_contacto','url')

        widgets = {
            "fecha_hora_inicio": forms.DateTimeInput(
                format=('%Y-%m-%dT%H:%M'),
                attrs={'class': 'form-control',
                       'type': 'datetime-local'
                       }),
            "fecha_hora_fin": forms.DateTimeInput(
                format=('%Y-%m-%dT%H:%M'),
                attrs={'class': 'form-control',
                       'type': 'datetime-local'
                       }),
            "correo":forms.EmailInput(),
            "descripcion": forms.Textarea(attrs={'rows': 4, 'cols': 15,'maxlength': '130'}),
            "celular": forms.NumberInput(attrs={'type': "tel", "pattern": "^(09)[0-9]{8}"}),
            "telefono": forms.NumberInput(attrs={'type': "tel", "pattern": "^(0)[1-9]{1}(\s){1}[0-9]{7}"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('titulo', css_class='col-6'),
                Column('descripcion', css_class='col-6'),
                Column('telefono', css_class='col-6'),
                Column('celular', css_class='col-6'),
                Column('correo', css_class='col-6'),
                Column('url', css_class='col-6'),
            ),
            Row(
                Column('nombre_contacto', css_class='col-6'),
                Column('fecha_hora_inicio', css_class='col-6'),
                Column('fecha_hora_fin', css_class='col-6'),
                Column('activo', css_class='col-6'),
                Column('imagen', css_class='col-6'),
            ),
        )
    def clean(self):
        cleaned_data = super(PromocionesForm, self).clean()
        fecha_hora_desde = cleaned_data.get("fecha_hora_inicio")
        fecha_hora_hasta = cleaned_data.get("fecha_hora_fin")
        if fecha_hora_desde and fecha_hora_hasta:
            if fecha_hora_hasta < fecha_hora_desde:
                raise forms.ValidationError(
                    "La fecha de fin no puede ser anterior a la fecha de inicio.")
        return cleaned_data