from crispy_forms.helper import FormHelper
from django import forms

from .models import *
import datetime
from crispy_forms.layout import Column, Div, Field, Layout, Row
from .widgets import DatePickerInput, TimePickerInput


class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        labels = {
            "imagen": "Logo del sponsor",
            "descripcion": "Descripción",
            "direccion": "Dirección de la matriz",
            'horario_cierre': "Horario de cierre de la matriz", 
            'horario_apertura': "Horario de apertura de la matriz",
            'correo': "Correo electrónico",
            'celular': "Teléfono móvil",
            'telefono':"Teléfono fijo"
        }
        fields = ('nombre','direccion', 'descripcion', 'telefono', 'nombre_contacto', 'url', 'imagen',
                  'fecha_inicio', 'fecha_fin', 'horario_apertura', 'horario_cierre', 'red_social','correo',"celular")

        widgets = {
            "imagen": forms.ClearableFileInput(),
            "descripcion": forms.Textarea(attrs={'rows': 4, 'cols': 15,'maxlength': '130'}),
            "fecha_inicio": forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'type': 'date'
                       }),
            "red_social":forms.TextInput(attrs={"pattern": "([a-zA-Z-1-9-@\.-_]+(,)?)+"}),
            "correo":forms.EmailInput(),
            "url": forms.URLInput(),
            "fecha_fin": forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'type': 'date'
                       }),
            'horario_apertura': TimePickerInput(),
            'horario_cierre': TimePickerInput(),
            "celular": forms.NumberInput(attrs={'type': "tel", "pattern": "^(09)[0-9]{8}"}),
            "telefono": forms.NumberInput(attrs={'type': "tel", "pattern": "^(0)[1-9]{1}(\s){1}[0-9]{7}"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-6'),
                Column('descripcion', css_class='col-6'),
                Column('telefono', css_class='col-6'),
                Column('celular', css_class='col-6'),
                Column('nombre_contacto', css_class='col-6'),
                Column('direccion', css_class='col-6'),
                Column('url', css_class='col-6'),
            ),
            Row(
                Column('correo', css_class='col-6'),
                Column('red_social', css_class='col-6'),
                Column('imagen', css_class='col-6'),
                Column('fecha_inicio', css_class='col-6 '),
                Column('fecha_fin', css_class='col-6 '),
                Column('horario_apertura', css_class='col-6'),
                Column('horario_cierre', css_class='col-6 '),
            ),
        )

    def clean(self):
        cleaned_data = super(SponsorForm, self).clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        hora_inicio = cleaned_data.get("horario_apertura")
        hora_fin = cleaned_data.get("horario_cierre")
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise forms.ValidationError(
                    "La fecha de fin no puede ser anterior a la fecha de inicio.")
        if hora_inicio and hora_fin:
            if hora_fin < hora_inicio:
                raise forms.ValidationError(
                    "La hora de cierre no puede ser anterior a la hora de apertura.")
        return cleaned_data
    

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        labels = {
            "imagen": "Imagen de la sucursal",
            'horario_cierre': "Horario de cierre de la sucursal", 
            'horario_apertura': "Horario de apertura de la sucursal",
            'correo':"Correo electrónico",
            'celular': "Teléfono móvil",
            'telefono':"Teléfono fijo",
            'direccion':"Dirección de la sucursal"
        }
        fields = ('nombre', 'telefono', 'imagen','fecha_inicio','fecha_fin',
                  'horario_apertura', 'horario_cierre', 'sponsor','correo','celular','direccion')

        widgets = {
            "fecha_inicio": forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'type': 'date'
                       }),
            "fecha_fin": forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'type': 'date'
                       }),
            "imagen": forms.ClearableFileInput(),
            "correo":forms.EmailInput(),
            'horario_apertura': TimePickerInput(),
            'horario_cierre': TimePickerInput(),
            "celular": forms.NumberInput(attrs={'type': "tel", "pattern": "^(09)[0-9]{8}"}),
            "telefono": forms.NumberInput(attrs={'type': "tel", "pattern": "^(0)[1-9]{1}(\s){1}[0-9]{7}"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-6'),
                Column('sponsor', css_class='col-6'),
                Column('telefono', css_class='col-6'),
                Column('celular', css_class='col-6'),
                Column('direccion', css_class='col-6'),
                Column('correo', css_class='col-6'),
            ),
            Row(
                Column('imagen', css_class='col-6'),
                Column('horario_apertura', css_class='col-6'),
                Column('horario_cierre', css_class='col-6 '),
                Column('fecha_inicio', css_class='col-6 '),
                Column('fecha_fin', css_class='col-6 '),
            ),
        )

    def clean(self):
        cleaned_data = super(SucursalForm, self).clean()
        hora_inicio = cleaned_data.get("horario_apertura")
        hora_fin = cleaned_data.get("horario_cierre")
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        if hora_inicio and hora_fin:
            if hora_fin < hora_inicio:
                raise forms.ValidationError(
                    "La hora de cierre no puede ser anterior a la hora de apertura.")
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise forms.ValidationError(
                    "La fecha de fin no puede ser anterior a la fecha de inicio.")
        return cleaned_data