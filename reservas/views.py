import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from calendario.filters import HorarioReservaFilter, MaquinaFilter, MaquinaReservaFilter
from calendario.forms import MaquinaForm
from calendario.models import Maquina,MaquinaReserva,HorarioReserva, PosicionMaquina
from django_filters.views import FilterView
from novagym.utils import calculate_pages_to_render
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect, render
from math import sqrt, ceil
import string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from seguridad.views import UsuarioPermissionRequieredMixin
# Create your views here.


class ListarMaquinas(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Maquina
    context_object_name = 'maquina'
    template_name = "templates/lista_maquina.html"
    permission_required = 'calendario.view_maquina'
    filterset_class=MaquinaFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "MÁQUINAS"
        page_obj = context["page_obj"]
        context['type'] = "m"
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CrearMaquina(LoginRequiredMixin, UsuarioPermissionRequieredMixin,CreateView):
    form_class =MaquinaForm
    model=Maquina
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('reservas:listarMaquinas')
    permission_required = 'calendario.add_maquina'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "CREAR MÁQUINA"
        return context

    def form_valid(self, form):
        response = super(CrearMaquina, self).form_valid(form)
        cantidad=self.object.cantidad
        abc = string.ascii_uppercase
        raiz= ceil(sqrt(cantidad))
        contador=0
        for i in abc[:cantidad]:     
            for k in range(1,raiz+1):
                if contador < cantidad:
                    PosicionMaquina.objects.create(fila=i,columna=str(k),maquina=self.object,zona=self.object.zona)
                    contador+=1
                else:
                    self.object.save()
                    break
        return response

class UpdateMaquina(LoginRequiredMixin, UsuarioPermissionRequieredMixin,UpdateView):
    form_class =MaquinaForm
    model=Maquina
    title = "ACTUALIZAR MÁQUINA"
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('reservas:listarMaquinas')
    permission_required = 'calendario.change_maquina'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Máquina"
        return context

class ListarReservasMaquinas(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = MaquinaReserva
    context_object_name = 'maquinaReserva'
    template_name = "templates/lista_maquinaReserva.html"
    permission_required = 'calendario.view_maquinareserva'
    filterset_class=MaquinaReservaFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "RESERVAS DE MÁQUINAS"
        page_obj = context["page_obj"]
        context['type'] = "m"
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ListarReservasHorarios(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = HorarioReserva
    context_object_name = 'horarioReserva'
    template_name = "templates/lista_horarioReserva.html"
    permission_required = 'calendario.view_horarioreserva'
    filterset_class=HorarioReservaFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "RESERVAS DE CLASES"
        page_obj = context["page_obj"]
        context['type'] = "c"
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@login_required
@permission_required('calendario.delete_maquina')
def deleteMaquina(request,id):
    query = Maquina.objects.get(id=id)
    try:
        if request.POST:
            query.imagen.delete()
            query.delete()
            messages.success(request, "Máquina eliminada con éxito.")
            return redirect('reservas:listarMaquinas')
        return render(request, "templates/ajax/maquina_confirmar_elminar.html", {"maquina": query})
    except:
        messages.error(request, "No se puede eliminar esta máquina.")
        return redirect('reservas:listarMaquinas')

@login_required
@permission_required('calendario.change_maquina')
def ChangeState(request,pk):
    query = Maquina.objects.get(id=pk)
    if request.POST:
        if query.activo==0:
            query.activo=1
            messages.success(request, "Máquina habilitada.")
            query.save()
            return redirect('reservas:listarMaquinas')
        elif query.activo==1:
            query.activo=0
            messages.error(request, "Máquina deshabilitada.")
            query.save()
            return redirect('reservas:listarMaquinas')
    return render(request, "templates/ajax/maquina_confirmar_change.html", {"maquina": query})

@login_required
@permission_required('calendario.change_maquina')
def changeReservable(request,pk):
    query = Maquina.objects.get(id=pk)

    if query.reservable==0:
        query.reservable=1
        #messages.success(request, "Máquina apta para reservas.")
        query.save()
        #return redirect('reservas:listarMaquinas')
    elif query.reservable==1:
        query.reservable=0
        #messages.error(request, "Máquina no apta para reservas.")
        query.save()
        #return redirect('reservas:listarMaquinas')

def showList(request,pk):
        hoy=datetime.datetime.today()
        queryset = MaquinaReserva.objects.filter(maquina=pk).filter(fecha=hoy)
        return render(request, "templates/ajax/maquinas_hoy.html", {"reservas": queryset})

def showListHorario(request,pk):
        hoy=datetime.datetime.today()
        queryset = HorarioReserva.objects.filter(horario=pk).filter(fecha=hoy)
        return render(request, "templates/ajax/horarios_hoy.html", {"reservas": queryset})