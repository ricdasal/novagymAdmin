from django.shortcuts import render
from django.forms import BooleanField
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django_filters.views import FilterView
from .forms import *
from .serializers import *
from django.core.mail import send_mail
from novagym.utils import calculate_pages_to_render
from datetime import date
from .models import *
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
# Create your views here.

@api_view(["GET"])
def calendarioList(request):
    calendario= Calendario.objects.all()
    serializer=CalendarioSerializer(calendario,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def calendarioDetail(request,id):
    calendario= Calendario.objects.get(id=id)
    serializer=CalendarioSerializer(calendario,many=False)
    return Response(serializer.data)

class ShowCalendario(FilterView):
    #paginate_by = 20
    #max_pages_render = 10
    model = Calendario
    context_object_name = 'calendario'
    template_name = "templates/lista_calendario.html"
    permission_required = 'novagym.view_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "CALENDARIO"
        #page_obj = context["page_obj"]
        #context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)