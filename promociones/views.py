import datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django_filters.views import FilterView
from httplib2 import Response
import pytz
from novagym.utils import calculate_pages_to_render
from promociones.filters import PromocionesFilter
from promociones.forms import PromocionesForm
from promociones.models import Promociones
from django.views.generic import CreateView, UpdateView
from rest_framework.views import APIView
from django.contrib import messages
from promociones.serializers import PublicidadSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class getPromociones(APIView):
    def get(self, request,activo=None, *args, **kwargs):
        data=Promociones.objects.all()
        if activo=="activo":
            queryset = data.filter(activo=1)
            serializer = PublicidadSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif activo=="inactivo":
            queryset = data.filter(activo=0)
            serializer = PublicidadSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif activo=="vigentes":
            today=datetime.datetime.now(tz=pytz.utc).strftime("%Y-%m-%dT%H:%M")
            queryset=Promociones.objects.filter(fecha_hora_inicio__lte=today).filter(fecha_hora_fin__gte=today)
            serializer = PublicidadSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        elif activo==None:
            serializer = PublicidadSerializer(data, many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(data="bad_request",status=status.HTTP_400_BAD_REQUEST)

class ListarPromociones(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Promociones
    context_object_name = 'promocion'
    template_name = "lista_promocion.html"
    permission_required = 'novagym.view_empleado'
    filterset_class=PromocionesFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "PUBLICIDAD"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class CrearPromociones(CreateView):
    form_class =PromocionesForm
    model=Promociones
    template_name = 'promocion_nuevo.html'
    success_url = reverse_lazy('promociones:listar')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "AGREGAR ANUNCIO"
        return context

def deletePromocion(request,id):
    query = Promociones.objects.get(id=id)
    if request.POST:
        query.imagen.delete()
        query.delete()
        messages.success(request, "Promoción eliminada con éxito.")
        return redirect('promociones:listar')
    return render(request, "ajax/promocion_confirmar_elminar.html", {"promocion": query})

class UpdatePromocion(UpdateView):
    form_class =PromocionesForm
    model=Promociones
    template_name = 'promocion_nuevo.html'
    success_url = reverse_lazy('promociones:listar')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "EDITAR ANUNCIO"
        return context

def ChangeState(request,pk):
    query = Promociones.objects.get(id=pk)
    if request.POST:
        if query.activo==0:
            query.activo=1
            messages.success(request, "Publicidad habilitada.")
            query.save()
            return redirect('promociones:listar')
        elif query.activo==1:
            query.activo=0
            messages.success(request, "Publicidad deshabilitada.")
            query.save()
            return redirect('promociones:listar')
    return render(request, "ajax/promocion_confirmar_change.html", {"promocion": query})