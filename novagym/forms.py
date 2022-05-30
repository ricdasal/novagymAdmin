from crispy_forms.helper import FormHelper
from django import forms
from crispy_forms.layout import Column, Layout, Row, Field, HTML
from crispy_forms.bootstrap import StrictButton


class TransaccionDolaresFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('usuario', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('estado', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column(
                    Field('created_at', template="forms/fields/range-filter.html",
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
