from crispy_forms.helper import FormHelper
from django import forms
from .models import *
from crispy_forms.layout import Column, Div, Field, Layout, Row
from .widgets import DateTimePickerInput

class NotificacionForm(forms.ModelForm):
    class Meta:
        model= Notificacion
        fields = ('titulo','cuerpo', 'imagen',"fecha_hora_inicio","fecha_hora_fin","frecuencia")

        widgets = {
            "imagen": forms.ClearableFileInput(),
            "cuerpo":forms.Textarea(attrs={'rows':4, 'cols':15}),
            "fecha_hora_inicio":DateTimePickerInput(),
            "fecha_hora_fin":DateTimePickerInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('titulo', css_class='col-6'),
                Column('imagen', css_class='col-6'),
                Column('cuerpo', css_class='col-6'),
            ),
            Row(
                Column('fecha_hora_inicio', css_class='col-6'),
                Column('fecha_hora_fin', css_class='col-6'),
                Column('frecuencia', css_class='col-6'),
            ),
        )