from crispy_forms.helper import FormHelper
from django import forms
from crispy_forms.layout import Column,Layout, Row, Field,HTML
from crispy_forms.bootstrap import StrictButton

class InputForm(forms.Form):
    cedula = forms.CharField(widget=forms.TextInput(attrs={"min":1,"max":5,'type':'number',"class":"textinput textInput form-control"}))
    codigo = forms.CharField(widget=forms.TextInput(attrs={"min":1,"max":5,'type':'number',"class":"form-control", "placeholder":"Código", "id":"inlineFormInputGroup"}))
