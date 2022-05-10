from crispy_forms.helper import FormHelper
from django import forms
from .models import Horario, HorarioHorario, HorarioMaquina, Maquina, Zona
from crispy_forms.layout import Column,Layout, Row, Field,HTML
from .widgets import TimePickerInput
from crispy_forms.bootstrap import StrictButton

class HorarioForm(forms.ModelForm):
    zona=forms.ModelChoiceField(queryset=Zona.objects.all().filter(tipo="clases"))
    class Meta:
        model= Horario
        labels = {
            "imagen": "Logo del sponsor",
            "descripcion": "Descripción de la actividad",
            "capacidadMaxima":"Capacidad"
        }
        fields = ('nombre', 'descripcion','gimnasio','capacidadMaxima','zona')

        widgets = {
            "descripcion":forms.Textarea(attrs={'rows':4, 'cols':15}),
            "capacidadMaxima":forms.NumberInput(attrs={'min':1})
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
                Column('capacidadMaxima', css_class='col-6'),
                Column('gimnasio', css_class='col-6'),
            ),
            Row(
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
    zona=forms.ModelChoiceField(queryset=Zona.objects.all().filter(tipo="maquinas"))
    class Meta:
        model= Maquina
        fields = ('nombre','descripcion','imagen','categoria','cantidad','reservable','activo','zona','gimnasio')
        
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
                Column('gimnasio', css_class='col-6'),
            ),
            Row(
                Column('zona', css_class='col-6'),
                Column(
                    HTML("""
                        <a href="{% url 'calendario:crearZona' %}"
                             class="btn btn-primary use-modal mr-2" >
                            <i class="fas fa-plus-circle"></i> Crear zona
                        </a>
                       """), css_class='col-auto align-self-end py-2'),
            ),  
            Row(
                Column('cantidad', css_class='col-6'),
                Column('imagen', css_class='col-6'),
                Column('activo', css_class='col-6'),
                Column('reservable', css_class='col-6'),
            ),
        )
class MaquinaFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('categoria', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('gimnasio', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
            ),
            Row(
                Column('zona',css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('reservable', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('activo',css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
            ),
            Row(
                Column(
                    StrictButton("Buscar", type='submit',css_class='btn btn-primary mt-1'),
                )
            ),
        )
class MaquinaReservaFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('usuario', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('maquina', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column(
                    Field('fecha', template="forms/fields/range-filter.html",
                          css_class="form-control"), css_class='col-12 col-md-6 col-lg-3'
                ),
            ),
            Row(
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )

class HorarioReservaFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('usuario', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('horario', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column(
                    Field('fecha', template="forms/fields/range-filter.html",
                          css_class="form-control"), css_class='col-12 col-md-6 col-lg-3'
                ),
            ),
            Row(
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )

class HorarioMaquinaForm(forms.ModelForm):
    class Meta:
        model= HorarioMaquina
        fields = ('dia','horario_inicio','horario_fin','maquina')
        widgets = {
                "horario_inicio":TimePickerInput,
                "horario_fin":TimePickerInput,
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('horario_inicio', css_class='col-6'),
                Column('horario_fin', css_class='col-6'),
            ),
            Row(
                Column('dia', css_class='col-6'),
                Column('maquina', css_class='col-6'),
            ),
        )

class HorarioHorarioForm(forms.ModelForm):
    class Meta:
        model= HorarioHorario
        fields = ('dia','horario_inicio','horario_fin','horario')
        labels={
            "horario":'Actividad'
        }
        widgets = {
                "horario_inicio":TimePickerInput,
                "horario_fin":TimePickerInput,
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('horario_inicio', css_class='col-6'),
                Column('horario_fin', css_class='col-6'),
            ),
            Row(
                Column('dia', css_class='col-6'),
                Column('horario', css_class='col-6'),
            ),
        )

class HorarioHorarioFilterForm(forms.ModelForm):
    class Meta:
        model= HorarioHorario
        fields = ('dia','horario')
        labels={
            "horario":'Actividad'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('dia', css_class='col-6'),
                Column('horario', css_class='col-6'),
            ),
            Row(
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )