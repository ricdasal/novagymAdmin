from crispy_forms.helper import FormHelper
from django import forms

from .models import *
import datetime
from crispy_forms.layout import Column, Div, Field, Layout, Row
from .widgets import DatePickerInput


class SponsorForm(forms.ModelForm):
    class Meta:
        model= Sponsor
        labels = {
            "imagen": "Logo del sponsor",
            "descripcion": "descripcion"
        }
        fields = ('nombre', 'descripcion', 'telefono', 'nombre_contacto', 'url','imagen','fecha_inicio','fecha_fin')

        widgets = {
            "imagen": forms.ClearableFileInput(),
            "descripcion":forms.Textarea(attrs={'rows':4, 'cols':15}),
            "fecha_inicio": forms.DateInput(attrs={
                'tabindex' : '1',
                'placeholder' : 'MM/DD/YYYY hh:mm',          
                'autocomplete':'off',}, format='%m/%d/%Y'),
            "url":forms.URLInput(),
            "fecha_fin": forms.DateInput(attrs={
                'tabindex' : '1',
                'placeholder' : 'MM/DD/YYYY hh:mm',          
                'autocomplete':'off',}, format='%m/%d/%Y'),
            "url":forms.URLInput(),
            "telefono": forms.NumberInput(attrs={'type':"tel","pattern":"^(09)[0-9]{8}"})
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
                Column('nombre_contacto', css_class='col-6'),
            ),
            Row(
                Column('url', css_class='col-6'),
                Column('imagen', css_class='col-6'),
                Column('fecha_inicio', css_class='col-6'),
                Column('fecha_fin', css_class='col-6 '),
            ),
        )

    def clean(self):
        cleaned_data = super(SponsorForm, self).clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise forms.ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")
            elif fecha_inicio < datetime.date.today():
                raise forms.ValidationError("La fecha de inicio no puede ser anterior a la fecha actual.")
        return cleaned_data

