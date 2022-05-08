from django.shortcuts import render
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from seguridad.views import UsuarioPermissionRequieredMixin
from afiliados.models import RegistroNovacoin
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

def entregarNovacoins(request):
    
    print(request)
    if request.POST:
        print("el pepe")
        print(request)
    return render(request, "otorgar.html")
    