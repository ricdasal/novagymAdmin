from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row
from django import forms

from .models import *


class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = ('titulo', 'cuerpo', 'imagen', "frecuencia", "fecha_inicio",
                  "fecha_fin", 'hora', 'nombre', 'tipo')
        labels = {
            'titulo': 'Título',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de fin'
        }
        widgets = {
            "cuerpo": forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            "hora": forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.fields['frecuencia'].help_text = "Seleccione 'Sin Frecuencia' si desea enviar manualmente estos mensajes"
        self.fields['tipo'].initial = Notificacion.Tipo.Admin
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column('nombre', css_class='col-12'),
                        Column('titulo', css_class='col-12'),
                        Column('cuerpo', css_class='col-12'),
                        Column('imagen', css_class='col-12'),
                    ), css_class='col-12 col-lg-6'),
                Column(
                    Row(
                        Column('frecuencia', css_class='col-12'),
                        Column('fecha_inicio', css_class='col-6'),
                        Column('fecha_fin', css_class='col-6'),
                        Column('hora', css_class='col-6'),
                        Column('tipo', css_class='d-none'),
                    ), css_class='col-12 col-lg-6'),
            ),
        )

    def clean_fecha_inicio(self):
        data = self.cleaned_data["fecha_inicio"]
        frecuencia = self.cleaned_data.get('frecuencia')
        if frecuencia != "NA" and not data:
            self.add_error('fecha_inicio', forms.ValidationError(
                'Frecuencia requiere una fecha de inicio'))
        return data

    def clean_fecha_fin(self):
        data = self.cleaned_data["fecha_fin"]
        frecuencia = self.cleaned_data.get('frecuencia')
        if frecuencia != "NA" and not data:
            self.add_error('fecha_fin', forms.ValidationError(
                'Frecuencia requiere una fecha de fin'))

        return data

    def clean_hora(self):
        data = self.cleaned_data["hora"]
        frecuencia = self.cleaned_data.get('frecuencia')
        if frecuencia != "NA" and not data:
            self.add_error('hora', forms.ValidationError(
                'Frecuencia requiere una hora'))
        return data

    def clean(self):
        cleaned_data = super().clean()
        frecuencia = cleaned_data.get('frecuencia')
        if frecuencia == "NA":
            cleaned_data["fecha_inicio"] = None
            cleaned_data["fecha_fin"] = None
            cleaned_data["hora"] = None
        return cleaned_data
