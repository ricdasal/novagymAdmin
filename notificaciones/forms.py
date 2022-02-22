from crispy_forms.helper import FormHelper
from django import forms
from .models import *
from crispy_forms.layout import Column, Div, Field, Layout, Row

class NotificacionForm(forms.ModelForm):
    class Meta:
        model= Notificacion
        fields = ('titulo','cuerpo', 'imagen')

        widgets = {
            "imagen": forms.ClearableFileInput(),
            "cuerpo":forms.Textarea(attrs={'rows':4, 'cols':15}),
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
            ),
            Row(
                Column('cuerpo', css_class='col-6'),
            ),
        )