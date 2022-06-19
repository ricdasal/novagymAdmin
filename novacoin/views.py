from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView
from novagym.utils import calculate_pages_to_render
from seguridad.views import UsuarioPermissionRequieredMixin

from novacoin.filters import RangoCambioCoinsFilter
from novacoin.forms import (MotivoCanjeForm, RangoCambioCoinsForm,
                            RecompensaForm)
from novacoin.models import DetalleCartera, RangoCambioCoins


# Create your views here.
class ListarRecompensas(LoginRequiredMixin, UsuarioPermissionRequieredMixin, FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = RangoCambioCoins
    context_object_name = 'recompensas'
    template_name = "lista_cambio_coins.html"
    permission_required = 'novacoins.view_rangocambiocoins'
    filterset_class = RangoCambioCoinsFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "NovaCoins"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(id=1)


class CrearRecompensa(LoginRequiredMixin, UsuarioPermissionRequieredMixin, CreateView):
    model = RangoCambioCoins
    form_class = RecompensaForm
    form_class_motivo = MotivoCanjeForm
    template_name = "recompensa_nc_nuevo.html"
    success_url = reverse_lazy('novacoin:listar')
    permission_required = 'novacoins.add_rangocambiocoins'
    title = "Agregar recompensa"

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "motivo_form" not in context:
            context["motivo_form"] = self.form_class_motivo
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST)
        form_motivo = self.form_class_motivo(request.POST)
        if form.is_valid() and form_motivo.is_valid():
            rango_cambio = form.save(commit=False)
            motivo = form_motivo.save()
            rango_cambio.motivo = motivo
            rango_cambio.save()
            messages.success(request, "Recompensa NC creada con éxito.")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response({"form": form, "motivo_form": form_motivo, "title": self.title})


class EditarRecompensa(LoginRequiredMixin, UsuarioPermissionRequieredMixin, UpdateView):
    model = RangoCambioCoins
    form_class = RecompensaForm
    form_class_motivo = MotivoCanjeForm
    template_name = "recompensa_nc_nuevo.html"
    success_url = reverse_lazy('novacoin:listar')
    permission_required = 'novacoins.change_rangocambiocoins'
    title = "Editar recompensa"

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "motivo_form" not in context:
            context["motivo_form"] = self.form_class_motivo(
                instance=self.object.motivo)
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        form_motivo = self.form_class_motivo(
            request.POST, instance=self.object.motivo)
        if form.is_valid() and form_motivo.is_valid():
            rango_cambio = form.save(commit=False)
            motivo = form_motivo.save()
            rango_cambio.motivo = motivo
            rango_cambio.save()
            messages.success(request, "Recompensa NC editada con éxito.")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response({"form": form, "motivo_form": form_motivo, "title": self.title})


@login_required
@permission_required('novacoin.delete_rangocambiocoins')
def changeState(request, pk):
    object = RangoCambioCoins.objects.get(id=pk)
    if request.POST:
        object.estado = not object.estado
        if object.estado:
            messages.success(request, "Recompensa NC habilitada con éxito.")
        else:
            messages.info(request, "Recompensa NC deshabilitada con éxito.")
        object.save()
        return redirect('novacoin:listar')
    if object.estado:
        return render(request, "ajax/recompensa_confirmar_elminar.html", {"object": object})
    return render(request, "ajax/recompensa_confirmar_activar.html", {"object": object})


@login_required
@permission_required('novacoin.delete_rangocambiocoins')
def deleteRecompensa(request, pk):
    object = RangoCambioCoins.objects.get(id=pk)
    if request.POST:
        object.delete()
        messages.info(request, "Recompensa NC eliminada con éxito.")
        return redirect('novacoin:listar')
    return render(request, "ajax/recompensa_confirmar_elminar_perma.html", {"object": object})


class EditarTasaCambio(LoginRequiredMixin, UsuarioPermissionRequieredMixin, UpdateView):
    model = RangoCambioCoins
    form_class = RangoCambioCoinsForm
    template_name = 'editar_rango_cambio_coins.html'
    success_url = reverse_lazy('novacoin:listar')
    permission_required = 'novacoins.change_rangocambiocoins'
    title = "Editar rango cambio"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def addCoinsToCartera(cartera, name_event):
    canje_existe = RangoCambioCoins.objects.filter(motivo__evento=name_event)
    if canje_existe.count():
        canje = canje_existe[0]
        if not(canje and canje.estado): return
        DetalleCartera.objects.create(
            cartera=cartera, motivo_canje=canje.motivo, coins_egreso=0, coins_ingreso=canje.coins)
        cartera.saldo_coins += canje.coins
        cartera.save()
