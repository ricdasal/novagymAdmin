from django.db import DataError
from django.shortcuts import render
from django.forms import BooleanField
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django_filters.views import FilterView
from rest_framework.views import APIView
from calendario.filters import CalendarioFilter
from .forms import *
from .serializers import *
from django.core.mail import send_mail
from novagym.utils import calculate_pages_to_render
from datetime import date
from .models import *
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.

@api_view(["GET"])
def calendarioList(request):
    calendario= Horario.objects.all()
    serializer=HorarioSerializer(calendario,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def calendarioDetail(request,id):
    calendario= Horario.objects.get(id=id)
    serializer=HorarioSerializer(calendario,many=False)
    return Response(serializer.data)


class Reservar(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        reserva = HorarioReservaSerializer(data=request.data, many=False, context={"request":request})
        idHorario=request.data["horario"]
        idUsuario=request.data["usuario"]
        reservado=HorarioReserva.objects.all().filter(horario_id=idHorario).filter(usuario_id=idUsuario)
        horario=Horario.objects.get(id=idHorario)
        if reserva.is_valid():
            if reservado:
                return Response(data="Sólo puede reservar la clase una vez", status=status.HTTP_200_OK)
            if horario.asistentes < horario.capacidad:
                horario.asistentes+=1
                horario.save()
                reserva.save()
            else:
                return Response(data="Horario lleno", status=status.HTTP_200_OK)
        return Response(reserva.data, status=status.HTTP_200_OK)

class ShowCalendario(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Horario
    context_object_name = 'calendario'
    template_name = "templates/lista_calendario.html"
    permission_required = 'novagym.view_empleado'
    filterset_class=CalendarioFilter

    def get_filterset_class(self):
        return self.filterset_class

    def filtering(self, request, *args, **kwargs):
        if request.GET.get('sucursales'):
            data=request.GET.get('sucursales')
            return data

    def get_queryset(self):
        return self.model.objects.filter(gimnasio=self.filtering(self.request))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "CALENDARIO"
        gimnasios=Gimnasio.objects.all()
        context["gimnasios"]=gimnasios
        #page_obj = context["page_obj"]
        #context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CrearCalendario(CreateView):
    form_class =HorarioForm
    model=Horario
    template_name = 'templates/calendario_nuevo.html'
    title = "AGREGAR ACTIVIDAD"
    success_url = reverse_lazy('calendario:listar')

class UpdateCalendario(UpdateView):
    form_class =HorarioForm
    model=Horario
    title = "ACTUALIZAR ACTIVIDAD"
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('calendario:listar')

def deleteCalendario(request,id):
    query = Horario.objects.get(id=id)
    if request.POST:
        query.delete()
        messages.success(request, "Actividad eliminada con éxito.")
        return redirect('calendario:listar')
    return render(request, "templates/ajax/calendario_confirmar_elminar.html", {"calendario": query})

def getHorarios(request):
    urls={}
    horarios=Horario.objects.all()
    for horario in horarios:
        if horario.gimnasio.nombre not in urls.keys():
            urls[horario.gimnasio.nombre]={
                "lunes":{},
                "martes":{},
                "miercoles":{},
                "jueves":{},
                "viernes":{},
                "sabado":{},
                "domingo":{}
                }
        urls[horario.gimnasio.nombre][str(horario.dia).lower()][horario.nombre]={
                "descripcion":horario.descripcion,
                "horaInicio":str(horario.horario_inicio),
                "horaFin":str(horario.horario_fin)
            }
    return HttpResponse(json.dumps(urls))