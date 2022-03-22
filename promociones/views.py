import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django_filters.views import FilterView
from novagym.utils import calculate_pages_to_render
from promociones.filters import PromocionesFilter
from promociones.forms import PromocionesForm
from promociones.models import Promociones
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
# Create your views here.

def getPromociones(request):
    promociones=Promociones.objects.all()
    urls={}
    for promocion in promociones:
        urls[promocion.titulo]={
                    "imagen":request.build_absolute_uri('/media/')+str(promocion.imagen),
                    "fecha_hora_inicio":str(promocion.fecha_hora_inicio),
                    "fecha_hora_fin":str(promocion.fecha_hora_fin),
                    "categoria":str(promocion.categoria),
                    "membresia":str(promocion.membresia),
                    }
    return HttpResponse(json.dumps(urls))

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
        context['title'] = "PROMOCIONES"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class CrearPromociones(CreateView):
    form_class =PromocionesForm
    model=Promociones
    template_name = 'promocion_nuevo.html'
    title = "CREAR PROMOCION"
    success_url = reverse_lazy('promociones:listar')

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
    title = "ACTUALIZAR PROMOCIÓN"
    template_name = 'promocion_nuevo.html'
    success_url = reverse_lazy('promociones:listar')

def ChangeState(request,pk):
    query = Promociones.objects.get(id=pk)
    if query.activo==0:
        query.activo=1
        messages.success(request, "Promocion "+query.titulo +" habilitada.")
    elif query.activo==1:
        query.activo=0
        messages.error(request, "Promocion "+query.titulo +" deshabilitada.")
    query.save()
    return redirect('promociones:listar')