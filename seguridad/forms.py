from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from seguridad.models import *


class UsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'groups']
        labels = {
          'groups': 'Rol'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['groups'].help_text = 'Use Ctrl para quitar o agregar al usuario a varios grupos.'
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='col-6'),
            ),
            Row(
                Column('password1', css_class='col-6'),
                Column('password2', css_class='col-6'),
            ),
            Row(
                Column('groups', css_class='col-6'),
            ),
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.save_m2m()
        return user


class UsuarioEditarForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'groups']
        labels = {
          'groups': 'Rol'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['groups'].help_text = 'Use Ctrl para quitar o agregar al usuario a varios grupos.'
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='col-6'),
            ),
            Row(
                Column('groups', css_class='col-6'),
            ),
        )


class UsuarioDetallesForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        exclude = ('usuario',)
        labels = {
            'cedula': "Cédula",
            'nombres': "Nombres",
            'apellidos': "Apellidos",
            'telefono': "Teléfono",
            'telefono2': "Teléfono secundario",
            'direccion': "Dirección",
            'sexo': "Sexo",
            "imagen": "Foto de perfil",
            "fecha_nacimiento": "Fecha de nacimento",
        }
        fields = '__all__'
        widgets = {
            "codigo": forms.HiddenInput(),
            "imagen": forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'codigo',
            Row(
                Column('imagen', css_class='col-6'),
                Column('tipo', css_class='col-4'),
            ),
            Row(
                Column('cedula', css_class='col-6 col-xl-4'),
                Column('nombres', css_class='col-6 col-xl-4'),
                Column('apellidos', css_class='col-6 col-xl-4'),
                Column('fecha_nacimiento', css_class='col-6 col-xl-4'),
                Column('telefono', css_class='col-6 col-xl-4'),
                Column('sexo', css_class='col-6 col-xl-4'),
            ),
        )


class UsuarioFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.fields['usuario__email'].label = "Email del usuario"
        self.fields['codigo'].label = "Código del usuario"
        self.fields['cedula'].label = "Cédula del usuario"
        self.fields['nombres'].label = "Nombres del usuario"
        self.fields['apellidos'].label = "Apellidos del usuario"
        self.fields['sexo'].label = "Sexo del empleado"
        self.fields['created_at'].label = "Fecha de ingreso"
        self.fields['rol'].label = "Rol del usuario"
        self.fields['tipo'].label = "Tipo de usuario"
        self.helper.layout = Layout(
            Row(
                Column('usuario__email', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('codigo', css_class='col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2'),
                Column('cedula', css_class='col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2'),
                Column('apellidos', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('nombres', css_class='col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2'),
                Column('tipo', css_class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2"),
                Column('rol', css_class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2"),
                Column('sexo', css_class='col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2'),
                Column(
                    Field('created_at', template="forms/fields/range-filter.html",
                          css_class="form-control"), css_class='col-12 col-md-6 col-lg-3'
                ),
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )
