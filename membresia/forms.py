from crispy_forms.bootstrap import PrependedText, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Layout, Row
from django import forms

from membresia.models import Beneficio, Membresia


class MembresiaFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre',
                       css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column(
                    'estado', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
            ),
            Row(
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )


class MembresiaForm(forms.ModelForm):
    class Meta:
        model = Membresia
        exclude = ('estado',)
        labels = {
            'descripcion': 'Descripción',
            'meses_duracion': 'Duración (meses)',
            'dias_duracion': 'Duración (dias)',
            'acceso_todo': 'Permitir acceso a todos los gimnasios',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('imagen', css_class='col-12 col-md-7')
            ),
            Row(
                Column('nombre', css_class='col-12 col-md-7'),
            ),
            Row(
                Column('descripcion', css_class='col-12 col-md-7'),
            ),
            Row(
                Column(PrependedText('precio', '$'),
                       css_class='col-6 col-md-3'),
                Column('meses_duracion', css_class='col-6 col-md-2'),
                Column('dias_duracion', css_class='col-6 col-md-2'),
            ),
            Row(
                Column(Field('beneficios', multiple="true",
                       css_class="select2"), css_class="col-12 col-md-7"),
                Column(
                    HTML("""
                        <a href="#" data-url="{% url 'membresia:listar_beneficio' %}" 
                            data-toggle='modal' data-target="#mainModal" class="btn btn-primary use-modal mr-2" >
                            <i class="fas fa-list"></i>
                        </a>
                       """), css_class='col-auto align-self-end py-2')
            ),
            Row(
              'acceso_todo'
            ),
        )

    def clean_meses_duracion(self):
        data = self.cleaned_data["meses_duracion"]
        if not data:
            data = 0
        return data

    def clean_dias_duracion(self):
        data = self.cleaned_data["dias_duracion"]
        if not data:
            data = 0
        return data

    def clean(self):
        cleaned_data = super().clean()
        meses_duracion = cleaned_data.get('meses_duracion')
        dias_duracion = cleaned_data.get('dias_duracion')
        if not (meses_duracion or dias_duracion):
            self.add_error('meses_duracion', forms.ValidationError(
                'Debe agregar al menos un valor en días o meses'))
        return cleaned_data


class BeneficioForm(forms.ModelForm):
    class Meta:
        model = Beneficio
        fields = '__all__'
        labels = {
            'texto': 'Descripción'
        }
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 2}),
        }
