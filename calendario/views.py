import string
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
from calendario.filters import CalendarioFilter, MaquinaFilter
from .forms import *
from .serializers import *
from .models import *
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from rest_framework.parsers import MultiPartParser, FormParser
from math import sqrt, ceil
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
        #reservado=HorarioReserva.objects.all().filter(horario_id=idHorario).filter(usuario_id=idUsuario)
        horario=Horario.objects.get(id=idHorario)
        idZona=horario.zona
        posiciones=Posicion.objects.all().filter(zona=idZona).filter(posicion=nroPosicion).get()
        if reserva.is_valid():
            #if reservado:
                #return Response(data="Sólo puede reservar la clase una vez", status=status.HTTP_200_OK)
            if horario.asistentes < horario.capacidad and posiciones.ocupado==False:
                posiciones.ocupado=True
                posiciones.save()
                horario.asistentes+=1
                horario.save()
                reserva.save()
                return Response(data=request.data, status=status.HTTP_200_OK)
            elif not posiciones:
                return Response(data="La posición es incorrecta o ya se ha reservado", status=status.HTTP_200_OK)
            elif horario.asistentes == horario.capacidad:
                return Response(data="Horario lleno", status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(data="Ocurrio un error", status=status.HTTP_200_OK)
        else:
            return Response(data="Ocurrio un error", status=status.HTTP_400_BAD_REQUEST)

class ReservarMaquina(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        idUsuario=request.data["usuario"]
        fila=request.data["fila"]
        columna=request.data["columna"]
        hora_inicio=request.data["horario_inicio"]
        hora_fin=request.data["horario_fin"]
        fecha=request.data["fecha"]
        maquina=request.data["maquina"]

        #reservado=MaquinaReserva.objects.all().filter(maquina_id=maquina).filter(usuario_id=idUsuario)
        posiciones=PosicionMaquina.objects.all().filter(maquina=maquina).filter(fila=fila).filter(columna=columna).get()
        newDict=request.data.copy()
        
        newDict["posicion"]=posiciones.id
        reserva = MaquinaReservaSerializer(data=newDict, many=False)

        if reserva.is_valid():
            #if reservado:
                #return Response(data="Sólo puede reservar este tipo de máquina una vez.", status=status.HTTP_200_OK)
            if posiciones.ocupado==False:
                posiciones.ocupado=True
                posiciones.save()
                reserva.save()
            elif not posiciones:
                return Response(data="La máquina es incorrecta o ya se ha reservado", status=status.HTTP_200_OK)
            elif posiciones.ocupado==True:
                return Response(data="Máquina no disponible", status=status.HTTP_403_FORBIDDEN)
            return Response(data=request.data, status=status.HTTP_200_OK)
        else:
            return Response(data="Ocurrio un error", status=status.HTTP_400_BAD_REQUEST)

class Horarios(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request,opcion=None, *args, **kwargs):
        if opcion==None:
            data=Horario.objects.all()
            serializer = HorarioSerializer(data, many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            data=Horario.objects.get(id=opcion)
            serializer = HorarioSerializer(data, many=False, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)

class HorariosReservas(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request,opcion=None, *args, **kwargs):
        if opcion==None:
            data=HorarioReserva.objects.all()
            serializer = HorarioReservaSerializer(data, many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return True      

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
        context['title'] = "HORARIOS"
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
        context['total'] = len(Zona.objects.all())
        context['clases'] = len(Zona.objects.all().filter(tipo="maquinas"))
        context['maquinas'] = len(Zona.objects.all().filter(tipo="clases"))
        return context

class UpdateZona(UpdateView):
    form_class =ZonaForm
    model=Zona
    title = "ACTUALIZAR ZONA"
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('calendario:listarZona')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Zona"
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
        tipo=self.object.tipo
        if tipo=="clases":
            for i in range(1,cantidad+1):
                Posicion.objects.create(posicion=i,zona=self.object)
        elif tipo=="maquinas":
            abc = string.ascii_uppercase
            raiz= ceil(sqrt(cantidad))
            contador=0
            for i in abc[:cantidad]:     
                for k in range(1,raiz+1):
                    if contador < cantidad:
                        PosicionMaquina.objects.create(fila=i,columna=str(k),zona=self.object)
                        contador+=1
                    else:
                        break
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

class MaquinasDispo(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request, *args, **kwargs):
        data=Maquina.objects.all()
        serializer = MaquinaDispoSerializer(data, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class HorariosDispo(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request, *args, **kwargs):
        data=Horario.objects.all()
        serializer = HorarioDispoSerializer(data, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class HorariosUsuario(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request,id, *args, **kwargs):
        data=HorarioReserva.objects.all().filter(usuario=id)
        serializer = ReporteHorarioReservaSerializer(data, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class MaquinaUsuario(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request,id, *args, **kwargs):
        data=MaquinaReserva.objects.all().filter(usuario=id)
        serializer = ReporteMaquinaReservaSerializer(data, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)