from email.mime.image import MIMEImage
from django.template import loader
from django.shortcuts import render
from django.shortcuts import render, redirect
from django_filters.views import FilterView
from contactenos.models import Buzon
from contactenos.filters import BuzonFilter
from novagym.utils import calculate_pages_to_render
from .forms import *
from django.core.mail import send_mail, BadHeaderError, mail_admins, EmailMultiAlternatives
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from backend.settings import env
from django.contrib import messages
from rest_framework.response import Response
from .serializers import BuzonSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.

class SendMail(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file_serializer = BuzonSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            titulo=request.POST.get('titulo')
            mensaje=request.POST.get('descripcion')
            img=request.FILES['imagen']
            imagen=img.open('rb')
            img_data = imagen.read()
            msg_img = MIMEImage(img_data)
            msg_img.add_header('Content-Disposition', "attachment; filename= %s" % str(img))
            msg = EmailMultiAlternatives(subject=titulo, body=mailContent(request,mensaje,msg_img),from_email= env("E_MAIL"),to= env.list("E_MAIL"))
            msg.attach(msg_img)
            msg.attach(logo_data())
            msg.content_subtype = 'html'
            imagen.close()
            msg.send()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowBuzon(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Buzon
    exclude = ['imagen']
    context_object_name = 'mail'
    template_name = "buzon.html"
    permission_required = 'seguridad.view_userdetails'
    filterset_class = BuzonFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "BUZÓN"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ShowBuzonNoLeidos(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Buzon
    exclude = ['imagen']
    context_object_name = 'mail'
    template_name = "buzonFilter.html"
    permission_required = 'seguridad.view_userdetails'
    filterset_class = BuzonFilter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "BUZÓN"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        context['theMail'] = Buzon.objects.filter(leido=0)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ShowBuzonLeidos(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Buzon
    exclude = ['imagen']
    context_object_name = 'mail'
    template_name = "buzonFilter.html"
    permission_required = 'seguridad.view_userdetails'
    filterset_class = BuzonFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "BUZÓN"
        
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        context['theMail'] = Buzon.objects.filter(leido=1)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

def deleteMail(request,id):
    query = Buzon.objects.get(id=id)
    if request.POST:
        query.imagen.delete()
        query.delete()
        messages.success(request, "Correo eliminado con éxito.")
        return redirect('contactenos:buzon')
    return render(request, "ajax/mail_confirmar_elminar.html", {"mail": query})

def mailContent(request,body,file):
    template=loader.get_template('mailTemplate.html')
    return template.render({"body": body})

def logo_data():
    with open("./static/images/logoBlack.png", "rb") as f:
        logo_data = f.read()
        logo = MIMEImage(logo_data)
        logo.add_header('Content-ID', '<logo>')
        return logo

def readMail(request,id):
    query = Buzon.objects.get(id=id)
    markAsRead(request,id)
    return render(request, "ajax/mail_leer.html", {"mail": query})

def markAsRead(request,id):
    mail=Buzon.objects.get(id=id)
    mail.leido=True
    mail.save()
    return redirect('contactenos:buzon')