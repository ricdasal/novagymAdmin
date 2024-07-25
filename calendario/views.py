from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import status
from rest_framework.response import Response
from django_filters.views import FilterView
from rest_framework.views import APIView
from calendario.filters import  HorarioHorarioFilter, HorarioMaquinaFilter
from .forms import *
from .serializers import *
from .models import *
from django.contrib import messages
import json
from django.views.generic import CreateView, UpdateView
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.mixins import LoginRequiredMixin
from seguridad.views import UsuarioPermissionRequieredMixin
from datetime import datetime
from rest_framework import generics
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
    #parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        reserva = HorarioReservaSerializer(data=request.data, many=False, context={"request":request})
        clase=request.data["clase"]
        idUsuario=request.data["usuario"]
        fecha=request.data["fecha"]
        horario=request.data["horario"]
        horarioHorario=HorarioHorario.objects.get(id=horario)
        hora_inicio=horarioHorario.horario_inicio
        hora_fin=horarioHorario.horario_fin
        otrasReservas=HorarioReserva.objects.filter(fecha=fecha).filter(usuario=idUsuario).filter(horario__horario_inicio__lte=hora_fin).filter(horario__horario_fin__gte=hora_inicio)
        reservado=HorarioReserva.objects.all().filter(fecha=fecha).filter(clase=clase).filter(usuario=idUsuario)
        horario=Horario.objects.get(id=clase)
        weekday=datetime.strptime(fecha,"%Y-%m-%d").weekday()
        fechaValida=int(horarioHorario.dia) == weekday
        estaReserva=len(HorarioReserva.objects.filter(fecha=fecha).filter(horario=clase))
        if reserva.is_valid():
            if len(reservado)>=1:
                return Response(data="Sólo puede reservar la clase una vez", status=status.HTTP_200_OK)
            if fechaValida==False:
                return Response(data="Fecha de reserva no válida", status=status.HTTP_200_OK)
            if estaReserva < horario.capacidad:
                if reserva.save():
                    instance=HorarioReserva.objects.get(id=reserva["id"].value)
                    serializer=HorarioReservaSerializer2(instance,many=False, context={"request":request})
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                else: 
                    return Response(data="No se pudo reservar", status=status.HTTP_200_OK)
            elif estaReserva == horario.capacidad:
                return Response(data="Horario lleno", status=status.HTTP_403_FORBIDDEN)
            elif len(otrasReservas)>0:
                return Response(data="Existe un cruce de horarios", status=status.HTTP_200_OK)
            else:
                return Response(data="Reserva no válida", status=status.HTTP_200_OK)
        else:
            return Response(data="Ocurrio un error", status=status.HTTP_400_BAD_REQUEST)

class ReservarMaquina(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        usuario=request.data["usuario"]
        fila=request.data["fila"]
        columna=request.data["columna"]
        horario=request.data["horario"]
        fecha=request.data["fecha"]
        maquina=request.data["maquina"]
        gimnasio=request.data["gimnasio"]

        horario=HorarioMaquina.objects.get(id=horario)
        hora_inicio=horario.horario_inicio
        hora_fin=horario.horario_fin
        reservados=MaquinaReserva.objects.filter(fecha=fecha).filter(gimnasio=gimnasio).filter(maquina=maquina).filter(horario=horario)
        reservaUsuario=reservados.filter(usuario=usuario)
        posiciones=PosicionMaquina.objects.filter(maquina=maquina)
        posicion=posiciones.filter(fila=fila).filter(columna=columna).get()
        otrasReservas=MaquinaReserva.objects.filter(fecha=fecha).filter(usuario=usuario).filter(horario__horario_inicio__lte=hora_fin).filter(horario__horario_fin__gte=hora_inicio)
        newDict=request.data.copy()
        newDict["posicion"]=posicion.id
        reserva = MaquinaReservaSerializer(data=newDict, many=False)

        weekday=datetime.strptime(fecha,"%Y-%m-%d").weekday()
        fechaValida=int(horario.dia) == weekday
        if reserva.is_valid():
            if len(reservaUsuario)>=1:
                return Response(data="Sólo puede reservar este tipo de máquina una vez.", status=status.HTTP_200_OK)
            if fechaValida==False:
                return Response(data="Fecha de reserva no válida", status=status.HTTP_200_OK)
            elif len(otrasReservas)>0:
                return Response(data="Existe un cruce de horarios", status=status.HTTP_200_OK)    
            elif len(reservados)>=len(posiciones):
                return Response(data="Horario lleno", status=status.HTTP_200_OK)
            for reservado in reservados:
                if reservado.posicion.id==posicion.id:
                    return Response(data="Máquina no disponible", status=status.HTTP_403_FORBIDDEN)
            else:
                reserva.save()
                instance=MaquinaReserva.objects.get(id=reserva["id"].value)
                serializer=MaquinaReservaSerializer2(instance,many=False, context={"request":request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data="Ocurrio un error", status=status.HTTP_400_BAD_REQUEST)

class Horarios(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def get(self, request,opcion=None, *args, **kwargs):
        if opcion==None:
            data=Horario.objects.all().filter(activo=True)
            serializer = HorarioSerializer(data, many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            data=Horario.objects.get(id=opcion)
            serializer = HorarioSerializer(data, many=False, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)

class HorariosReservas(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def get(self, request,opcion=None, *args, **kwargs):
        if opcion==None:
            data=HorarioReserva.objects.all()
            serializer = HorarioReservaSerializer(data, many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return True      



class ShowCalendario(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    model = HorarioHorario
    context_object_name = 'horarios'
    template_name = "templates/lista_calendario.html"
    permission_required = 'calendario.view_horario'
    filterset_class=HorarioHorarioFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Horarios de actividades"
        context['type']="c"
        return context

class ShowMaquinaHorario(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    model = HorarioMaquina
    context_object_name = 'horarios'
    template_name = "templates/lista_calendarioMaquina.html"
    permission_required = 'calendario.view_horario'
    filterset_class=HorarioMaquinaFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Horarios de actividades"
        context['type']="m"
        return context

class ListarActividades(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    model = Horario
    context_object_name = 'actividades'
    template_name = "templates/lista_actividades.html"
    permission_required = 'calendario.view_horario'
    #filterset_class=CalendarioFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actividades"
        gimnasios=Gimnasio.objects.all()
        context["gimnasios"]=gimnasios
        return context

class CrearHorarioHorario(LoginRequiredMixin, UsuarioPermissionRequieredMixin,CreateView):
    form_class =HorarioHorarioForm
    model=HorarioHorario
    template_name = 'templates/horariohorario_nuevo.html'
    success_url = reverse_lazy('calendario:listar')
    permission_required = 'calendario.add_maquina'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Agregar Horario"
        return context

class EditarHorarioMaquina(LoginRequiredMixin, UsuarioPermissionRequieredMixin,UpdateView):
    form_class =HorarioMaquinaForm
    model=HorarioMaquina
    template_name = 'templates/horariohorario_nuevo.html'
    success_url = reverse_lazy('calendario:listarHorarioMaquina')
    permission_required = 'calendario.change_maquina'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar Horario"
        return context

class CrearHorarioMaquina(LoginRequiredMixin, UsuarioPermissionRequieredMixin,CreateView):
    form_class =HorarioMaquinaForm
    model=HorarioMaquina
    template_name = 'templates/horariomaquina_nuevo.html'
    success_url = reverse_lazy('reservas:listarHorarioMaquina')
    permission_required = 'calendario.add_maquina'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Agregar Horario"
        return context
    

class CrearCalendario(LoginRequiredMixin, UsuarioPermissionRequieredMixin,CreateView):
    form_class =HorarioForm
    model=Horario
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('calendario:listar')
    permission_required = 'calendario.add_horario'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Agregar actividad"
        return context

class UpdateCalendario(LoginRequiredMixin, UsuarioPermissionRequieredMixin,UpdateView):
    form_class =HorarioForm
    model=Horario
    title = "ACTUALIZAR ACTIVIDAD"
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('calendario:listar')
    permission_required = 'calendario.change_horario'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar actividad"
        return context

class UpdateHorarioHorario(LoginRequiredMixin, UsuarioPermissionRequieredMixin,UpdateView):
    form_class =HorarioHorarioForm
    model=HorarioHorario
    title = "Actualizar horario"
    template_name = 'templates/horariohorario_nuevo.html'
    success_url = reverse_lazy('calendario:listarActividades')
    permission_required = 'calendario.change_horario'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar actividad"
        return context

@login_required
@permission_required('calendario.delete_horario')
def deleteHorarioHorario(request,id):
    try:
        query = HorarioHorario.objects.get(id=id)
        if request.POST:
            query.delete()
            messages.success(request, "Horario eliminado con éxito.")
            return redirect('calendario:listar')
        return render(request, "templates/ajax/horario_confirmar_elminar.html", {"horario": query})
    except:
        messages.error(request, "No se puede eliminar este horario.")
        return redirect('calendario:listar')

@login_required
@permission_required('calendario.delete_maquina')
def deleteHorarioMaquina(request,id):
    try:
        query = HorarioMaquina.objects.get(id=id)
        if request.POST:
            query.delete()
            messages.success(request, "Horario eliminado con éxito.")
            return redirect('calendario:listarHorarioMaquina')
        return render(request, "templates/ajax/horarioMaquina_confirmar_elminar.html", {"horario": query})
    except:
        messages.error(request, "No se puede eliminar este horario.")
        return redirect('calendario:listarHorarioMaquina')

@login_required
@permission_required('calendario.change_horario')
def ChangeState(request,pk):
    query = Horario.objects.get(id=pk)
    if request.POST:
        if query.activo==0:
            query.activo=1
            messages.success(request, "Horario habilitado.")
            query.save()
            return redirect('calendario:listarActividades')
        elif query.activo==1:
            query.activo=0
            messages.error(request, "Horario deshabilitado.")
            query.save()
            return redirect('calendario:listarActividades')
    return render(request, "templates/ajax/horario_confirmar_change.html", {"actividad": query})

class ShowZona(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Zona
    context_object_name = 'zona'
    template_name = "templates/lista_zona.html"
    permission_required = 'calendario.view_zona'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "LISTAR ZONAS"
        context['total'] = len(Zona.objects.all())
        context['clases'] = len(Zona.objects.all().filter(tipo="maquinas"))
        context['maquinas'] = len(Zona.objects.all().filter(tipo="clases"))
        return context

@login_required
@permission_required('calendario.delete_zona')
def deleteZona(request,id):
    try:
        query = Zona.objects.get(id=id)
        if request.POST:
            query.delete()
            messages.success(request, "Zona eliminada con éxito.")
            return redirect('calendario:listarZona')
        return render(request, "templates/ajax/zona_confirmar_elminar.html", {"zona": query})
    except:
        messages.error(request, "No se puede eliminar esta zona.")
        return redirect('calendario:listarZona')

class UpdateZona(LoginRequiredMixin, UsuarioPermissionRequieredMixin,UpdateView):
    form_class =ZonaForm
    model=Zona
    title = "ACTUALIZAR ZONA"
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('calendario:listarZona')
    permission_required = 'calendario.change_zona'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Zona"
        return context

class CrearZona(LoginRequiredMixin, UsuarioPermissionRequieredMixin,CreateView):
    form_class =ZonaForm
    model=Zona
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('calendario:listarZona')
    permission_required = 'calendario.add_zona'
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
        return response

@login_required
@permission_required('calendario.delete_horario')
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
    #parser_classes = (MultiPartParser, FormParser)
    def get(self, request, *args, **kwargs):
        data=Maquina.objects.all()
        serializer = MaquinaDispoSerializer(data, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class HorariosDispo(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def get(self, request, *args, **kwargs):
        data=Horario.objects.all()
        serializer = HorarioDispoSerializer(data, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class HorariosUsuario(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def get(self, request,id, *args, **kwargs):
        data=HorarioReserva.objects.all().filter(usuario=id)
        data2=MaquinaReserva.objects.all().filter(usuario=id)
        serializer = ReporteHorarioReservaSerializer(data, many=True)
        serializer2 = ReporteMaquinaReservaSerializer(data2, many=True)
        
        #dataMix={"clases":serializer.data,"maquinas":serializer2.data}
        return Response(serializer.data+serializer2.data,status=status.HTTP_200_OK)

class MaquinaUsuario(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def get(self, request,id, *args, **kwargs):
        data=MaquinaReserva.objects.all().filter(usuario=id)
        serializer = ReporteMaquinaReservaSerializer(data, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class HorarioSmall(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def get(self, request,opc=None, *args, **kwargs):
        if opc==None:
            data=Horario.objects.all().filter(activo=True)
            serializer = HorarioSmallSerializer(data, many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            data=Horario.objects.get(id=opc)
            serializer = HorarioSmallSerializer(data, many=False, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)

class DisponibilidadMaquina(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        maquinaId=request.data["maquina"]
        fecha=request.data["fecha"]
        lista=[]
        reservas=MaquinaReserva.objects.filter(fecha=fecha).filter(maquina=maquinaId)
        valores=reservas.values_list("posicion", flat=True)
        maquinas=PosicionMaquina.objects.all().filter(maquina=maquinaId)
        for maquina in maquinas:
            id=maquina.id
            fila=maquina.fila
            columna=maquina.columna
            if id in valores:
                lista.append({"id":id,"fila":fila,"columna":columna,"ocupado":True})
            else:
                lista.append({"id":id,"fila":fila,"columna":columna,"ocupado":False})

        return Response(lista,content_type='application/json',status=status.HTTP_200_OK)

class HorariosDispo(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        idHorario=request.data["horario"]
        fecha=request.data["fecha"]
        horario=Horario.objects.get(id=idHorario)
        capacidad=horario.capacidad
        data=HorarioReserva.objects.all().filter(fecha=fecha).filter(horario=idHorario)
        disponibles=capacidad-len(data)
        datas={'id':horario.id,'nombre':horario.nombre,'aforo':str(horario.gimnasio.aforo)+"%",'espacios':capacidad,'disponibles':disponibles}
        #serializer = HorarioReservaSerializer(data, many=True)
        return Response(data=datas,status=status.HTTP_200_OK)

class VerificarMaquina(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        fecha=request.data["fecha"]
        gimnasio=request.data["gimnasio"]
        hora=request.data["hora"]
        maquina=request.data["maquina"]
        reservas=MaquinaReserva.objects.all().filter(fecha=fecha).filter(maquina=maquina).filter(horario_inicio=hora).filter(gimnasio=gimnasio)
        espacios=PosicionMaquina.objects.all().filter(maquina=maquina)
        if len(reservas)<len(espacios):
            data={'reservas':len(reservas),'espacios':len(espacios),'completo':False}
            return Response(data=data,status=status.HTTP_200_OK)
        else:
            data={'reservas':len(reservas),'espacios':len(espacios),'completo':True}
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)

class VerHorariosMaquinas(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        fecha=request.data["fecha"]
        gimnasio=request.data["gimnasio"]
        weekday=datetime.strptime(fecha,"%Y-%m-%d").weekday()
        try:
            maquina=request.data["maquina"]
            horarios=HorarioMaquina.objects.filter(dia=weekday).filter(maquina__gimnasio=gimnasio).filter(maquina=maquina)
            serializer=HorarioMaquinaSerializer(horarios,many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        except:
            horarios=HorarioMaquina.objects.filter(dia=weekday).filter(maquina__gimnasio=gimnasio)
            serializer=HorarioMaquinaSerializer(horarios,many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)

class VerHorariosClase(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        fecha=request.data["fecha"]
        gimnasio=request.data["gimnasio"]
        weekday=datetime.strptime(fecha,"%Y-%m-%d").weekday()
        try:
            horario=request.data["horario"]
            horarios=HorarioHorario.objects.filter(dia=weekday).filter(horario__gimnasio=gimnasio).filter(horario=horario)
            serializer=HorarioHorarioSerializer(horarios,many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)

        except:
            horarios=HorarioHorario.objects.filter(dia=weekday).filter(horario__gimnasio=gimnasio)
            serializer=HorarioHorarioSerializer(horarios,many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)

class HorarioHorarioList(generics.ListAPIView):
    queryset = HorarioHorario.objects.all()
    serializer_class = HorarioHorarioSerializer

class HorarioHorarioByNombre(generics.ListAPIView):
    serializer_class = HorarioHorarioSerializer

    def get_queryset(self):
        horario_nombre = self.kwargs.get('horario_nombre')
        id_gimnasio = self.kwargs.get('id_gimnasio')

        current_date = datetime.today()
        # Obtener el día de la semana (0=Lunes, 6=Domingo)
        day_of_week = current_date.weekday()
        return HorarioHorario.objects.filter(horario__nombre=horario_nombre, horario__gimnasio_id=id_gimnasio, dia=day_of_week)

class HorarioMaquinaDetailView(generics.RetrieveAPIView):
    queryset = HorarioMaquina.objects.all()
    serializer_class = HorarioMaquinaSerializer

class HorarioMaquinaListCreateView(generics.ListCreateAPIView):
    queryset = HorarioMaquina.objects.all()
    serializer_class = HorarioMaquinaSerializer

class HorarioMaquinaByCategoriaView(generics.ListAPIView):
    serializer_class = HorarioMaquinaSerializer

    def get_queryset(self):
        categoria = self.kwargs.get('categoria')
        id_gimnasio = self.kwargs.get('id_gimnasio')

        # Obtener la fecha actual
        current_date = datetime.today()
        # Obtener el día de la semana (0=Lunes, 6=Domingo)
        day_of_week = current_date.weekday()
        # Mapeo de número de día a string
        dia_map = {
            0: 'LUNES',
            1: 'MARTES',
            2: 'MIERCOLES',
            3: 'JUEVES',
            4: 'VIERNES',
            5: 'SABADO',
            6: 'DOMINGO'
        }
        dia_str = dia_map.get(day_of_week)

        # Filtrar el queryset por categoría, gimnasio y día de la semana
        return HorarioMaquina.objects.filter(
            maquina__categoria=categoria,
            maquina__gimnasio_id=id_gimnasio,
            dia=day_of_week
        )