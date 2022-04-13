from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.views import FilterView
from backend.settings import env
from gimnasio.filters import GimnasioFilter
from .forms import *
from .serializers import *
from novagym.utils import calculate_pages_to_render
from .models import *
from django.contrib import messages
from django.views.generic import CreateView, UpdateView

# Create your views here.
#Gimnasio - Contacto

class ListarGimnasio(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Gimnasio
    context_object_name = 'gimnasio'
    template_name = "lista_gimnasio.html"
    permission_required = 'novagym.view_empleado'
    filterset_class=GimnasioFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "GIMNASIOS"
        page_obj = context["page_obj"]
        context["total"]=Gimnasio.objects.all().count()
        context["activos"]=Gimnasio.objects.filter(estado=True).count()
        context["inactivos"]=Gimnasio.objects.filter(estado=False).count()
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CrearGimnasio(CreateView):
    form_class =GimnasioForm
    model=Gimnasio
    template_name = 'gimnasio_nuevo.html'
    title = "CREAR SPONSOR"
    success_url = reverse_lazy('gimnasio:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Agregar Gimnasio"
        context['crear'] =1
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            valid=self.form_valid(form)
            gymId=Gimnasio.objects.latest('id').id
            aforo=request.POST.get('aforo')
            capacidad=request.POST.get('capacidad')
            calcularAforo(gymId,aforo,capacidad)
            return valid
        else:
            return self.form_invalid(form)

class UpdateGimnasio(UpdateView):
    form_class =GimnasioForm
    model=Gimnasio
    title = "ACTUALIZAR GIMNASIO"
    template_name = 'gimnasio_nuevo.html'
    success_url = reverse_lazy('gimnasio:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Gimnasio"
        context['crear'] = 0
        #context['key'] = env("MAPS_API_KEY")
        return context

    def post(self, request, *args, **kwargs):
        gimnasio = self.get_object().id
        aforo=request.POST.get('aforo')
        capacidad=request.POST.get('capacidad')
        calcularAforo(gimnasio,aforo,capacidad)
        messages.success(request, "Gimnasio actualizado con éxito.")
        return super(UpdateGimnasio, self).post(request, *args, **kwargs)

def deleteGimnasio(request,id):
    query = Gimnasio.objects.get(id=id)
    if request.POST:
        try:
            query.delete()
        except:
            messages.error(request, "Imposible eliminar. Existen horarios pertenecientes al gimnasio")
            return redirect('gimnasio:listar')
        messages.success(request, "Gimnasio eliminado con éxito.")
        return redirect('gimnasio:listar')
    return render(request, "ajax/gimnasio_confirmar_elminar.html", {"gimnasio": query})

def changeState(request,pk):
    gimnasio=Gimnasio.objects.get(id=pk)
    if request.POST:
        if gimnasio.estado:
            gimnasio.estado=False
            messages.error(request, "Gimnasio "+gimnasio.nombre +" deshabilitado.")
            gimnasio.save()
            return redirect('gimnasio:listar')
        else:
            gimnasio.estado=True
            messages.success(request, "Gimnasio "+gimnasio.nombre +" habilitado.")
            gimnasio.save()
            return redirect('gimnasio:listar')
    return render(request, "ajax/gimnasio_confirmar_change.html", {"gimnasio": gimnasio})

def changeAforo(request):
    gimnasios=Gimnasio.objects.all()
    aforoGlobal = request.GET.get('aforo')
    if aforoGlobal:
        for gimnasio in gimnasios:
            gimnasio.aforo=aforoGlobal
            gimnasio.save()
            calcularAforo(gimnasio.id,gimnasio.aforo,gimnasio.capacidad)
    return redirect('gimnasio:listar')

class GetGimnasios(APIView):
    def get(self, request,opc=None, *args, **kwargs):
        if opc==None:
            queryset=Gimnasio.objects.all()
            serializer=GimnasioSerializer(queryset,many=True, context={"request":request})
            if serializer:
                return Response(data=serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(data="algo salio mal",status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset=Gimnasio.objects.get(id=opc)
            serializer=GimnasioSerializer(queryset,many=False, context={"request":request})
            if serializer:
                return Response(data=serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(data="algo salio mal",status=status.HTTP_400_BAD_REQUEST)

def calcularAforo(id,aforo,capacidad):
    gimnasio=Gimnasio.objects.get(id=int(id))
    gimnasio.personas=int(capacidad)*(int(aforo)/100)
    gimnasio.save()