from crispy_forms.layout import Column,Layout, Row
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton

class MaquinaReservaFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('fecha', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('usuario', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('maquina', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
            )
        )