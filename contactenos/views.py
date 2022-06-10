from email.mime.image import MIMEImage
from django.template import loader
from django.shortcuts import render
from django.shortcuts import render, redirect
from django_filters.views import FilterView
from contactenos.models import Buzon
from contactenos.filters import BuzonFilter
from novagym.utils import calculate_pages_to_render
from .forms import *
from django.core.mail import EmailMultiAlternatives
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from backend.settings import env
from django.contrib import messages
from rest_framework.response import Response
from .serializers import BuzonSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.mixins import LoginRequiredMixin
from seguridad.views import UsuarioPermissionRequieredMixin
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

class SendMail(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file_serializer = BuzonSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            titulo=request.POST.get('titulo')
            mensaje=request.POST.get('descripcion')
            try:
                img=request.FILES['imagen']
                imagen=img.open('rb')
                img_data = imagen.read()
                msg_img = MIMEImage(img_data)
                msg_img.add_header('Content-Disposition', "attachment; filename= %s" % str(img))
                msg = EmailMultiAlternatives(subject=titulo, body=mailContent(request,mensaje),from_email= env("E_MAIL"),to= env.list("E_MAIL"))
                msg.attach(msg_img)
                #msg.attach(logo_data())
                imagen.close()
            except:
                msg = EmailMultiAlternatives(subject=titulo, body=mailContent(request,mensaje),from_email= env("E_MAIL"),to= env.list("E_MAIL"))
            msg.content_subtype = 'html'
            msg.send()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CorreoBienvenida(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        correo=request.POST.get('correo')
        try:
            msg = EmailMultiAlternatives(subject="Bienvenido a Novagym!", body=bienvenidaMailContent(request),from_email= env("E_MAIL"),to=[correo])
            msg.content_subtype = 'html'
            msg.send()
            return Response("Bienvenida enviada", status=status.HTTP_200_OK)
        except:
            return Response("Ocurrió un error", status=status.HTTP_400_BAD_REQUEST)

class ShowBuzon(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Buzon
    exclude = ['imagen']
    context_object_name = 'mail'
    template_name = "buzon.html"
    permission_required = 'contactenos.view_buzon'
    filterset_class = BuzonFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "BUZÓN"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ShowBuzonNoLeidos(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Buzon
    exclude = ['imagen']
    context_object_name = 'mail'
    template_name = "buzonFilter.html"
    permission_required = 'contactenos.view_buzon'
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

class ShowBuzonLeidos(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Buzon
    exclude = ['imagen']
    context_object_name = 'mail'
    template_name = "buzonFilter.html"
    permission_required = 'contactenos.view_buzon'
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

@login_required
@permission_required('contactenos.delete_buzon')
def deleteMail(request,id):
    query = Buzon.objects.get(id=id)
    if request.POST:
        query.imagen.delete()
        query.delete()
        messages.success(request, "Correo eliminado con éxito.")
        return redirect('contactenos:buzon')
    return render(request, "ajax/mail_confirmar_elminar.html", {"mail": query})

def mailContent(request,body):
    template=loader.get_template('mailTemplate.html')
    return template.render({"body": body})

def bienvenidaMailContent(request,username="Usuario"):
    template=loader.get_template('bienvenidaMailTemplate.html')
    return template.render({"body": username})

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