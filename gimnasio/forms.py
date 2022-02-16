from crispy_forms.helper import FormHelper
from django import forms
from .models import *

class GimnasioForm(forms.ModelForm):
    class Meta:
        model = Gimnasio
        labels = {
            "imagen": "Imagen de referencia"
        }
        widgets = {
            "imagen": forms.ClearableFileInput(),
        }
        fields = ('tipo','nombre', 'imagen','telefono','ubicacion','horario_inicio', 'horario_fin','estado','ciudad')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False