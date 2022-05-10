import datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django_filters.views import FilterView
from httplib2 import Response
import pytz
from novagym.filters import TransaccionDolaresFilter
from novagym.models import DetalleTransaccionProducto, Transaccion
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
from django.contrib.auth.mixins import LoginRequiredMixin
from seguridad.views import UsuarioPermissionRequieredMixin
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

class ListarTransaccionDolares(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    #paginate_by = 20
    #max_pages_render = 10
    model = Transaccion
    context_object_name = 'transacciones'
    template_name = "lista_transacciondolares.html"
    permission_required = 'novagym.view_transaccion'
    filterset_class=TransaccionDolaresFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Transacciones ($)"
        context['tipo']='dolares'
        #page_obj = context["page_obj"]
        #context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ListarTransaccionCoins(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    #paginate_by = 20
    #max_pages_render = 10
    model = Transaccion
    context_object_name = 'transacciones'
    template_name = "lista_transacciondolares.html"
    permission_required = 'novagym.view_transaccion'
    filterset_class=TransaccionDolaresFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Transacciones (Novacoins)"
        context['tipo']='novacoins'
        #page_obj = context["page_obj"]
        #context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@login_required
@permission_required("novagym.view_transaccion")
def verProductos(request,id):
    query = DetalleTransaccionProducto.objects.filter(transaccion=id)
    return render(request, "ajax/verProductos.html", {"queryset": query,"transaccion":id})