from crispy_forms.helper import FormHelper
from django import forms
from .models import *
from crispy_forms.layout import Column, Div, Field, Layout, Row
class SponsorForm(forms.ModelForm):
    class Meta:
        model= Sponsor
        labels = {
            "imagen": "Logo del sponsor",
            "descripcion": "descripcion"
        }
        fields = ('codigo','nombre', 'descripcion', 'telefono', 'nombre_contacto', 'url','imagen','fecha_inicio','fecha_fin')

        widgets = {
            "imagen": forms.ClearableFileInput(),
            "descripcion":forms.Textarea(attrs={'rows':4, 'cols':15}),
            "fecha_inicio": forms.SelectDateWidget(attrs={'style': 'display: inline-block; width: 33%;'}),
            "fecha_fin": forms.SelectDateWidget(attrs={'style': 'display: inline-block; width: 33%;'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('codigo', css_class='col-6'),
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