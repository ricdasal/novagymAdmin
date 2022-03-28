from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_filters.views import FilterView
from django.views.generic import UpdateView
from django.contrib import messages

from decimal import Decimal, DecimalException

from novagym.utils import calculate_pages_to_render

from .models import AlmacenamientoGlobal, AlmacenamientoUsuario
from .utils import validar_number

class AlmacenamientoUsuarioView(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = AlmacenamientoUsuario
    queryset = AlmacenamientoUsuario.objects.all().order_by('usuario')
    context_object_name = 'almacenamiento_usuarios'
    template_name = "lista_almacenamiento_usuarios.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        almacenamiento_global, created = AlmacenamientoGlobal.objects.get_or_create(id=1)
        context['almacenamiento_global'] = almacenamiento_global
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AdministrarExcepcionesView(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = AlmacenamientoUsuario
    queryset = AlmacenamientoUsuario.objects.filter(es_excepcion=True).order_by('usuario')
    context_object_name = 'administrar_excepciones'
    template_name = "administrar_excepciones.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        almacenamiento_global = AlmacenamientoGlobal.objects.get(id=1)
        context['almacenamiento_global'] = almacenamiento_global
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


def configurar_almacenamiento(request):
    almacenamiento_global = AlmacenamientoGlobal.objects.get(id=1)
    context = {
        'almacenamiento_global': almacenamiento_global
    }

    if request.POST:
        sin_limite = request.POST.get('sin_limite')
        if sin_limite:
            almacenamiento_global.sin_limite = True
        else:
            try:
                servidor = validar_number(request.POST.get('servidor'))
                nueva_capacidad_max = validar_number(request.POST.get('capacidad_max'))
                nuevo_peso_archivo_max = validar_number(request.POST.get('peso_archivo_max'))
            except DecimalException:
                messages.error(request, 'Error al guardar los valores.')
                return render(request, 'configurar_almacenamiento.html', context)

            #modificar el almacenamiento asignado a los usuarios
            almacenamiento_usuarios = AlmacenamientoUsuario.objects.all()
            for almacenamiento_user in almacenamiento_usuarios:
                if not almacenamiento_user.es_excepcion:
                    if almacenamiento_user.asignado == almacenamiento_global.capacidad_max:
                        almacenamiento_user.asignado = nueva_capacidad_max
                    if almacenamiento_user.peso_archivo_asignado == almacenamiento_global.peso_archivo_max:
                        almacenamiento_user.peso_archivo_asignado = nuevo_peso_archivo_max
                    almacenamiento_user.save()

            almacenamiento_global.servidor = servidor
            almacenamiento_global.capacidad_max = nueva_capacidad_max
            almacenamiento_global.peso_archivo_max = nuevo_peso_archivo_max
            almacenamiento_global.sin_limite = False
        almacenamiento_global.save()

        messages.success(request, 'Operacion realizada con exito.')
        return redirect('almacenamiento:almacenamiento_usuario')

    return render(request, 'configurar_almacenamiento.html', context)


def configurar_usuario(request, user):
    almacenamiento_usuario = AlmacenamientoUsuario.objects.get(usuario=user)
    context = {
        'almacenamiento_usuario': almacenamiento_usuario
    }
    return render(request, 'configurar_almacenamiento_usuario.html', context)


def modificar_almacenamiento_usuario(request, user, page):
    almacenamiento_usuario = AlmacenamientoUsuario.objects.get(usuario=user)
    if request.POST:
        try:
            nuevo_asignado = validar_number(request.POST.get('asignado'))
            nuevo_peso_archivo_asignado = validar_number(request.POST.get('peso_archivo_asignado'))
        except DecimalException:
            messages.error(request, 'Error al guardar los valores.')
            if page == 'excepcion':
                return redirect('almacenamiento:administrar_excepciones')
            else:
                return redirect('almacenamiento:configurar_usuario', user=almacenamiento_usuario.usuario.id)


        if nuevo_asignado != almacenamiento_usuario.asignado or nuevo_peso_archivo_asignado != almacenamiento_usuario.peso_archivo_asignado:
            almacenamiento_usuario.es_excepcion = True

        almacenamiento_global = AlmacenamientoGlobal.objects.get(id=1)
        if almacenamiento_global.capacidad_max == nuevo_asignado and almacenamiento_global.peso_archivo_max == nuevo_peso_archivo_asignado:
            almacenamiento_usuario.es_excepcion = False

        almacenamiento_usuario.asignado = nuevo_asignado
        almacenamiento_usuario.peso_archivo_asignado = nuevo_peso_archivo_asignado
        almacenamiento_usuario.save()

        messages.success(request, 'Operacion realizada con exito.')
        return redirect('almacenamiento:almacenamiento_usuario')




