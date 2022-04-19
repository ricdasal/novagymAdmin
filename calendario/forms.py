from crispy_forms.helper import FormHelper
from django import forms
from .models import Horario, Maquina, Zona
from crispy_forms.layout import Column,Layout, Row
from .widgets import TimePickerInput

class HorarioForm(forms.ModelForm):
    class Meta:
        model= Horario
        labels = {
            "imagen": "Logo del sponsor",
            "descripcion": "Descripción de la actividad"
        }
        fields = ('dia','nombre', 'descripcion','horario_inicio','horario_fin','gimnasio','capacidad','zona')

        widgets = {
            "descripcion":forms.Textarea(attrs={'rows':4, 'cols':15}),
            "horario_inicio": TimePickerInput(),
            "horario_fin": TimePickerInput(),
            "capacidad":forms.NumberInput(attrs={'min':1})
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
                Column('capacidad', css_class='col-6'),
            ),
            Row(
                Column('gimnasio', css_class='col-6'),
                Column('horario_inicio', css_class='col-6'),
                Column('horario_fin', css_class='col-6 '),
                Column('zona', css_class='col-6 '),
            ),
        )
    def clean(self):
        cleaned_data = super(HorarioForm, self).clean()
        horario_inicio = cleaned_data.get("horario_inicio")
        horario_fin = cleaned_data.get("horario_fin")
        if horario_inicio and horario_fin:
            if horario_fin < horario_inicio:
                raise forms.ValidationError("La hora de inicio no puede ser anterior a la hora de fin.")
        return cleaned_data

class ZonaForm(forms.ModelForm):
    class Meta:
        model= Zona
        fields = ('nombre', 'espacios','tipo')
        widgets = {
                "espacios":forms.NumberInput(attrs={'min':1})
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-6'),
                Column('espacios', css_class='col-6'),
            ),
            Row(
                Column('tipo', css_class='col-6'),
            ),
        )

class MaquinaForm(forms.ModelForm):
    class Meta:
        model= Maquina
        fields = ('nombre','descripcion','imagen','categoria','cantidad','reservable','activo','zona')
        widgets = {
                "cantidad":forms.NumberInput(attrs={'min':1}),
                "descripcion": forms.Textarea(attrs={'rows': 4, 'cols': 15,'maxlength': '130'})
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-6'),
                Column('categoria', css_class='col-6'),
                Column('descripcion', css_class='col-6'),
                Column('zona', css_class='col-6'),
            ),
            Row(
                Column('cantidad', css_class='col-6'),
                Column('reservable', css_class='col-6'),
                Column('activo', css_class='col-6'),
                Column('imagen', css_class='col-6'),
            ),
        )