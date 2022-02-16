from django import forms

# Create your forms here.

class ContactForm(forms.Form):
	nombre = forms.CharField(max_length = 50)
	apellido = forms.CharField(max_length = 50)
	email = forms.EmailField(max_length = 150)
	mensaje = forms.CharField(widget = forms.Textarea, max_length = 2000)