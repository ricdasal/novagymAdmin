import io
from pyexpat.errors import messages
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView

from novagym.utils import calculate_pages_to_render
from comunidad.utils import enum_media

from .models import ArchivoPublicacion, Publicacion
from .forms import PublicacionForm, ArchivoFormSet

import base64


class ListaPublicacionReportada(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Publicacion
    queryset = Publicacion.objects.filter(visible=False).all()
    context_object_name = 'publicacion_reportada'
    template_name = "lista_publicacion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Publicaciones Reportadas"
        context['tipo'] = "reporte"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListaPublicacionNovagym(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Publicacion
    queryset = Publicacion.objects.filter(usuario__is_superuser=1).all()
    context_object_name = 'publicacion_novagym'
    template_name = "lista_publicacion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Publicaciones Reportadas"
        context['tipo'] = "novagym"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CrearPublicacion(CreateView):
    form_class = PublicacionForm
    template_name = 'nueva_publicacion.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        if self.request.POST:
            print("POST del get context")
            data['archivos'] = ArchivoFormSet(self.request.POST, self.request.FILES)
        else:
            data['archivos'] = ArchivoFormSet()
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['archivos']
        if form.is_valid() and formset.is_valid():
            form.instance.usuario = self.request.user
            self.object = form.save()
            for f in formset:
                file = f.cleaned_data['archivo'] 
                archivo = ArchivoPublicacion(publicacion=self.object, archivo=file)
                archivo.almacenamiento_utilizado = round(file.size/1000, 2)
                type = file.content_type.split("/")
                #verificar que el tipo sea solo img, vid, aud
                archivo.tipo = enum_media[type[0]]
                archivo.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("comunidad:publicacion_novagym")


def aceptar_publicacion(request, pk):
    if request.POST:
        print("listo para eliminar")
        messages.success(request, 'Operacion realizada con exito.')
    print("llegando")
    return render(request, 'ajax/aceptar_publicacion.html', {'publicacion': pk})