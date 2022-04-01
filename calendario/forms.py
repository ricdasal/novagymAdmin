from crispy_forms.helper import FormHelper
from django import forms
from .models import Calendario
from crispy_forms.layout import Column, Div, Field, Layout, Row
from .widgets import TimePickerInput

class CalendarioForm(forms.ModelForm):
    class Meta:
        model= Calendario
        labels = {
            "imagen": "Logo del sponsor",
            "descripcion": "Descripción de la actividad"
        }
        fields = ('dia','nombre', 'descripcion','horario_inicio','horario_fin','gimnasio')

        widgets = {
            "descripcion":forms.Textarea(attrs={'rows':4, 'cols':15}),
            "horario_inicio": TimePickerInput(),
            "horario_fin": TimePickerInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('dia', css_class='col-6'),
                Column('nombre', css_class='col-6'),
                Column('descripcion', css_class='col-6'),
            ),
            Row(
                Column('gimnasio', css_class='col-6'),
                Column('horario_inicio', css_class='col-6'),
                Column('horario_fin', css_class='col-6 '),
            ),
        )
    def clean(self):
        cleaned_data = super(CalendarioForm, self).clean()
        horario_inicio = cleaned_data.get("horario_inicio")
        horario_fin = cleaned_data.get("horario_fin")
        if horario_inicio and horario_fin:
            if horario_fin < horario_inicio:
                raise forms.ValidationError("La hora de inicio no puede ser anterior a la hora de fin.")
        return cleaned_data