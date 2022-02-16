from crispy_forms.helper import FormHelper
from django import forms
from .models import *

class SponsorForm(forms.ModelForm):
    class Meta:
        model= Sponsor
        labels = {
            "imagen": "Logo del sponsor",
            "descripcion": "descripcion"
        }
        widgets = {
            "imagen": forms.ClearableFileInput(),
            "descripcion":forms.Textarea(),
            "fecha_inicio": forms.SelectDateWidget(),
            "fecha_fin": forms.SelectDateWidget()
        }
        fields = ('codigo','nombre', 'descripcion', 'telefono', 'nombre_contacto', 'url','imagen','fecha_inicio','fecha_fin')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
