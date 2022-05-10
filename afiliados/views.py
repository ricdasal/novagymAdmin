from warnings import catch_warnings
from django.shortcuts import redirect, render
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from afiliados.forms import InputForm
from novacoin.models import Cartera, DetalleCartera, MotivoCanje, RangoCambioCoins
from seguridad.models import UserDetails
from seguridad.views import UsuarioPermissionRequieredMixin
from afiliados.models import RegistroNovacoin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from sponsor.models import Sponsor
# Create your views here.

class ListarRegistro(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = RegistroNovacoin
    context_object_name = 'registro'
    template_name = "templates/lista_registro.html"
    permission_required = 'novagym.view_empleado'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registro de novacoins otorgadas"
        return context

@login_required
@permission_required('sponsor.view_sponsor')
def entregarNovacoins(request):
    context ={}
    form=InputForm(request.POST or None)
    context['form']= form
    context['title']= "Entregar Novacoins"
    if request.POST:
        if form.is_valid():
            cedula = form.cleaned_data.get("cedula")
            codigo = form.cleaned_data.get("codigo")
            try:
                cambio=RangoCambioCoins.objects.get(id=1)
                usuario=UserDetails.objects.get(cedula=cedula)
                cartera=Cartera.objects.get(usuario=usuario.id)
                sponsor=Sponsor.objects.get(codigo="SPR-"+str(codigo))
                motivo=MotivoCanje.objects.get(id=1)
                cartera.saldo_coins+=cambio.coins
                cartera.save()
                detallecartera=DetalleCartera.objects.create(cartera=cartera,motivo_canje=motivo,coins_egreso=0,coins_ingreso=cambio.coins)
                messages.success(request, "Novacoins entregadas con éxito.")
                return redirect('afiliados:entregar')
            except:
                messages.error(request, "Error al entregar Novacoins.")
                return redirect('afiliados:entregar') 
    return render(request, "otorgar.html",context)
    