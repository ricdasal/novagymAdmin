from cgitb import text
from cProfile import label

from crispy_forms.bootstrap import AppendedText, PrependedText, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Field, Layout, Row
from django import forms

from novacoin.models import MotivoCanje, RangoCambioCoins


class RangoCambioCoinsFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.fields['nombre'].label = "Nombre"
        self.fields['created_at'].label = "Fecha de creación"
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-md-6 col-lg-3'),
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
            )
        )


class RecompensaForm(forms.ModelForm):
    class Meta:
        model = RangoCambioCoins
        exclude = ('monto_minimo', 'monto_maximo', 'estado', 'motivo')
        labels = {
            "texto": "Descripción",
            "coins": "Recompensa",
        }
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('texto', css_class='col-12 col-xl-8'),
            ),
            Row(
                Column(
                    AppendedText('coins', 'NovaCoins'), css_class='col-12 col-xl-4'),
            )
        )


class MotivoCanjeForm(forms.ModelForm):
    class Meta:
        model = MotivoCanje
        exclude = ('estado', 'tipo_movimiento',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(Column('nombre', css_class='col-12 col-xl-8'))
        )


class RangoCambioCoinsForm(forms.ModelForm):
    class Meta:
        model = RangoCambioCoins
        exclude = ('estado', 'texto')
        labels = {
            'monto_minimo': '',
            'monto_maximo': '',
            'coins': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.fields['monto_minimo'].required = True
        self.helper.layout = Layout(
            Row(
                HTML("<div style='align-self: center;'>Cada</div>"),
                Column(
                    PrependedText('monto_minimo', '$'), css_class='col-6 col-xl-4'
                ),
                HTML('<div style="align-self: center;">gastados <i class="fas fa-arrow-right"></i> Obtiene </div>'),
                Column(
                    AppendedText('coins', 'NovaCoins'), 
                    css_class='col-6 col-xl-4'
                ),
            ),
            Row(
                HTML("<div style='align-self: center;'>Monto máximo por compra</div>"),
                Column(
                    PrependedText('monto_maximo', '$'), css_class='col-6 col-xl-4'
                ),
                Column('motivo', css_class='d-none'),
                css_class="mt-5"
            )
        )
    def clean(self):
        cleaned_data = super().clean()
        monto_minimo = cleaned_data.get('monto_minimo')
        monto_maximo = cleaned_data.get('monto_maximo')
        if monto_maximo and monto_minimo and monto_maximo < monto_minimo:
            self.add_error('monto_maximo', forms.ValidationError(
                    'El monto máximo debe ser mayor o igual a ${}'.format(monto_minimo)))
        return cleaned_data