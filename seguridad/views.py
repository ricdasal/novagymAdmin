from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (AccessMixin, LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView
from novagym.utils import calculate_pages_to_render

from seguridad.filters import UsuarioFilter
from seguridad.forms import UsuarioDetallesForm, UsuarioEditarForm, UsuarioForm

from .models import *

# Admin


def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.POST.get('next', None)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('novagym:principal')
            else:
                messages.error(request, 'Esta cuenta ha sido desactivada.')
                return redirect('seguridad:login_admin')
        else:
            messages.error(
                request, 'Nombre de usuario o contraseña incorrecto.')
            return redirect('seguridad:login_admin')
    else:
        if request.user and request.user.is_authenticated:
            return redirect('novagym:principal')
        else:
            return render(request, 'login.html', {"title": "Iniciar Sesión"})


def logout_user(request):
    if request.GET:
        logout(request)
        return redirect('seguridad:login_admin')


class UsuarioPermissionRequieredMixin(PermissionRequiredMixin, AccessMixin):
    raise_exception = False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )


class ListarUsuarios(LoginRequiredMixin, UsuarioPermissionRequieredMixin, FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = UserDetails
    context_object_name = 'usuarios'
    template_name = "lista_usuarios.html"
    permission_required = 'novagym.view_user_details'
    filterset_class = UsuarioFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Usuarios"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CrearUsuario(LoginRequiredMixin, UsuarioPermissionRequieredMixin, CreateView):
    model = UserDetails
    form_class = UsuarioDetallesForm
    user_form_class = UsuarioForm
    template_name = 'usuario_nuevo.html'
    title = "Crear usuario"
    success_url = reverse_lazy('seguridad:listar')
    permission_required = 'novagym.add_usuario'

    def get_context_data(self, **kwargs):
        context = super(CrearUsuario, self).get_context_data(**kwargs)
        if "user_form" not in context:
            context['user_form'] = self.user_form_class()
        if "form" not in context:
            context['form'] = self.form_class()
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        usuario_form = self.user_form_class(request.POST)
        usuario_detalles_form = self.form_class(request.POST)
        if usuario_form.is_valid() and usuario_detalles_form.is_valid():
            user = usuario_form.save(commit=False)
            user.username = user.email
            user.save()
            detalles = usuario_detalles_form.save(commit=False)
            try:
                pre = str(int(self.model.objects.latest('pk').pk+1))
                sec = '0'*(4-len(pre))+pre
            except self.model.DoesNotExist:
                sec = '0001'
            detalles.codigo = sec
            detalles.usuario = user
            detalles.save()
            messages.success(request, "Usuario creado con éxito.")
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response({"form": usuario_detalles_form, "user_form": usuario_form,
                                            "title": self.title})


class EditarUsuario(LoginRequiredMixin, UsuarioPermissionRequieredMixin, UpdateView):
    model = UserDetails
    form_class = UsuarioDetallesForm
    user_form_class = UsuarioEditarForm
    template_name = 'usuario_nuevo.html'
    title = "Editar usuario"
    success_url = reverse_lazy('seguridad:listar')
    permission_required = 'novagym.change_usuario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "user_form" not in context:
            context['user_form'] = self.user_form_class(
                instance=self.object.usuario)
        if "form" not in context:
            context['form'] = self.form_class(
                instance=self.object.detalles)
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario_detalles_form = self.form_class(
            request.POST, request.FILES, instance=self.object)
        usuario_form = self.user_form_class(
            request.POST, instance=self.object.usuario)
        if usuario_form.is_valid() and usuario_detalles_form.is_valid():
            user = usuario_form.save()
            detalles = usuario_detalles_form.save(commit=False)
            detalles.usuario = user
            detalles.save()
            messages.success(request, "Usuario editado con éxito.")
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response({"form": usuario_detalles_form, "user_form": usuario_form,
                                            "title": self.title})


@login_required()
def usuario_confirmar_eliminacion(request, pk):
    detalles = UserDetails.objects.get(id=pk)
    if request.POST:
        usuario = detalles.usuario
        usuario.is_active = False
        usuario.save()
        messages.success(request, "Usuario deshabilitado con éxito.")
        return redirect('seguridad:listar')
    return render(request, "ajax/usuario_confirmar_elminar.html", {"usuario": detalles})


@login_required()
def usuario_confirmar_activar(request, pk):
    detalles = UserDetails.objects.get(id=pk)
    if request.POST:
        usuario = detalles.usuario
        usuario.is_active = True
        usuario.save()
        messages.success(request, "Usuario habilitado con éxito.")
        return redirect('seguridad:listar')
    return render(request, "ajax/usuario_confirmar_activar.html", {"usuario": detalles})
