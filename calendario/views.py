from django.shortcuts import render
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
        nroPosicion=request.data["posicion"]
        
        reservado=HorarioReserva.objects.all().filter(horario_id=idHorario).filter(usuario_id=idUsuario)
        horario=Horario.objects.get(id=idHorario)
        idZona=horario.zona
        posiciones=Posicion.objects.all().filter(zona=idZona).filter(posicion=nroPosicion).get()
        if reserva.is_valid():
            if reservado:
                return Response(data="Sólo puede reservar la clase una vez", status=status.HTTP_200_OK)
            if horario.asistentes < horario.capacidad and posiciones.ocupado==False:
                posiciones.ocupado=True
                posiciones.save()
                horario.asistentes+=1
                horario.save()
                
                reserva.save()
                
            if not posiciones:
                return Response(data="La posición es incorrecta o ya se ha reservado", status=status.HTTP_200_OK)
            if horario.asistentes == horario.capacidad:
                return Response(data="Horario lleno", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(data=request.data, status=status.HTTP_200_OK)
        else:
            return Response(data="Ocurrio un error", status=status.HTTP_400_BAD_REQUEST)

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
    success_url = reverse_lazy('calendario:listar')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "AGREGAR ACTIVIDAD"
        return context

class UpdateCalendario(UpdateView):
    form_class =HorarioForm
    model=Horario
    title = "ACTUALIZAR ACTIVIDAD"
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('calendario:listar')
    
class ShowZona(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Zona
    context_object_name = 'zona'
    template_name = "templates/lista_zona.html"
    permission_required = 'novagym.view_empleado'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "LISTAR ZONAS"
        return context

class CrearZona(CreateView):
    form_class =ZonaForm
    model=Zona
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('calendario:listarZona')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "CREAR ZONA"
        return context

    def form_valid(self, form):
        response = super(CrearZona, self).form_valid(form)
        cantidad=self.object.espacios
        for i in range(1,cantidad+1):
            Posicion.objects.create(posicion=i,zona=self.object)
        return response

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