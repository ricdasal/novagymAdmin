from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import *
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from seguridad import views

# Create your views here.

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Dudas y sugerencias" 
			body = {
			'nombre': form.cleaned_data['nombre'], 
			'apellido': form.cleaned_data['apellido'], 
			'email': form.cleaned_data['email'], 
			'mensaje':form.cleaned_data['mensaje'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ("seguridad:login_admin")
      
	form = ContactForm()
	return render(request, "contacto.html", {'form':form})