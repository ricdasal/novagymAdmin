from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.response import Response
from django_filters.views import FilterView
from .forms import *
from .serializers import *
from novagym.utils import calculate_pages_to_render
from .models import *
from django.contrib import messages
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import CreateView, UpdateView
from .filters import SponsorFilter, SucursalFilter
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from seguridad.views import UsuarioPermissionRequieredMixin
# Create your views here.
#SPONSOR

def redesParser(serializer):
    newData=serializer.data
    redes=newData['red_social'].split(",")
    lista={}
    for red in redes:
        token=red.split(":")
        lista[token[0]]=token[1]
    newData['red_social']=lista
    return newData
    
class sponsorList(APIView):
    def get(self, request,activo=None, *args, **kwargs):
        if activo=="activo":
            queryset = Sponsor.objects.all().filter(activo=1)
            serializer = SponsorSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif activo=="inactivo":
            queryset = Sponsor.objects.all().filter(activo=0)
            serializer = SponsorSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif activo=="todos":
            queryset = Sponsor.objects.all()
            serializer = SponsorSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif activo=="vigentes":
            today=datetime.datetime.now().strftime("%Y-%m-%d")
            queryset=Sponsor.objects.filter(fecha_inicio__lte=today).filter(fecha_fin__gte=today).filter(activo=True)
            serializer = SponsorSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        elif activo==None:
            queryset=Sponsor.objects.all()
            serializer = SponsorSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(data="bad_request",status=status.HTTP_400_BAD_REQUEST)

class sucursalList(APIView):
    def get(self, request,activo=None, *args, **kwargs):
        if activo=="activo":
            queryset = Sucursal.objects.all().filter(activo=1)
            serializer = SucursalSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif activo=="inactivo":
            queryset = Sucursal.objects.all().filter(activo=0)
            serializer = SucursalSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif activo=="todos":
            queryset = Sucursal.objects.all()
            serializer = SucursalSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif activo=="vigentes":
            today=datetime.datetime.now().strftime("%Y-%m-%d")
            queryset=Sucursal.objects.filter(fecha_inicio__lte=today).filter(fecha_fin__gte=today).filter(activo=True)
            serializer = SucursalSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        elif activo==None:
            queryset=Sucursal.objects.all()
            serializer = SucursalSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(data="bad_request",status=status.HTTP_400_BAD_REQUEST)

class sucursalDetail(APIView):
    def get(self, request,id, *args, **kwargs):
        if id:
            queryset = Sucursal.objects.all().filter(sponsor=id)
            serializer = SucursalSerializer(queryset, many=True, context={"request":request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data="bad_request",status=status.HTTP_400_BAD_REQUEST)
            
class sponsorDetail(APIView):
    def get(self, request,id, *args, **kwargs):
        queryset = Sponsor.objects.get(id=id)
        serializer = SponsorSerializer(queryset, many=False, context={"request":request})
        if queryset.red_social:
            data=redesParser(serializer)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        


def createSponsor(request):
    if request.method=='POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sponsor:createSponsor")
    else:
        form=SponsorForm()
    return render(request,'createSponsor.html',{'form':form})

class ListarSponsors(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Sponsor
    context_object_name = 'sponsor'
    template_name = "lista_sponsor.html"
    permission_required = 'sponsor.view_sponsor'
    filterset_class=SponsorFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "ANUNCIANTES"
        page_obj = context["page_obj"]
        context["total"]=Sponsor.objects.all().count()
        context["activos"]=Sponsor.objects.filter(activo=True).count()
        context["inactivos"]=Sponsor.objects.filter(activo=False).count()
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@login_required
@permission_required('sponsor.delete_sponsor')
def deleteSponsor(request,id):
    query = Sponsor.objects.get(id=id)
    if request.POST:
        query.imagen.delete()
        query.delete()
        messages.success(request, "Anunciante eliminado con éxito.")
        return redirect('sponsor:listar')
    return render(request, "ajax/sponsor_confirmar_elminar.html", {"sponsor": query})

class CrearSponsor(LoginRequiredMixin, UsuarioPermissionRequieredMixin,CreateView):
    form_class =SponsorForm
    model=Sponsor
    template_name = 'sponsor_nuevo.html'
    title = "CREAR ANUNCIANTE"
    success_url = reverse_lazy('sponsor:listar')
    permission_required = 'sponsor.add_sponsor'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Agregar Anunciante"
        return context

class UpdateSponsor(LoginRequiredMixin, UsuarioPermissionRequieredMixin,UpdateView):
    form_class =SponsorForm
    model=Sponsor
    title = "ACTUALIZAR SPONSOR"
    template_name = 'sponsor_nuevo.html'
    success_url = reverse_lazy('sponsor:listar')
    permission_required = 'sponsor.change_sponsor'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Anunciante"
        return context

class ListarSucursales(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Sucursal
    context_object_name = 'sucursal'
    template_name = "lista_sucursal.html"
    permission_required = 'sponsor.view_sucursal'
    filterset_class=SucursalFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SUCURSALES"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        context['sponsors'] = Sponsor.objects.all()
        context["total"]=Sucursal.objects.all().count()
        context["activos"]=Sucursal.objects.filter(activo=True).count()
        context["inactivos"]=Sucursal.objects.filter(activo=False).count()
        return context

    def filtering(self, request, *args, **kwargs):
        if request.GET.get('sucursales'):
            data=request.GET.get('sucursales')
            return data

    def get_queryset(self):
        filtro=self.filtering(self.request)
        if filtro=='all':
            return self.model.objects.all()
        return self.model.objects.filter(sponsor=filtro)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UpdateSucursal(UpdateView):
    form_class =SucursalForm
    model=Sucursal
    title = "ACTUALIZAR SUCURSAL"
    template_name = 'sponsor_nuevo.html'
    success_url = reverse_lazy('sponsor:listarSucursal')
    permission_required = 'sponsor.change_sucursal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Sucursal"
        return context


class CrearSucursal(CreateView):
    form_class =SucursalForm
    model=Sucursal
    template_name = 'sponsor_nuevo.html'
    title = "CREAR SUCURSAL"
    success_url = reverse_lazy('sponsor:listarSucursal')
    permission_required = 'sponsor.add_sucursal'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Agregar Sucursal"
        return context

@login_required
@permission_required('sponsor.delete_sucursal')
def deleteSucursal(request,id):
    query = Sucursal.objects.get(id=id)
    if request.POST:
        query.imagen.delete()
        query.delete()
        messages.success(request, "Sucursal eliminada con éxito.")
        return redirect('sponsor:listarSucursal')
    return render(request, "ajax/sucursal_confirmar_elminar.html", {"sucursal": query})

@login_required
@permission_required('sponsor.change_sponsor')
def ChangeState(request,pk):
    query = Sponsor.objects.get(id=pk)
    if request.POST:
        if query.activo==0:
            query.activo=1
            messages.success(request, "Anunciante "+query.nombre +" habilitado.")
            query.save()
            return redirect('sponsor:listar')
        elif query.activo==1:
            query.activo=0
            messages.success(request, "Anunciante "+query.nombre +" deshabilitado.")
            query.save()
            return redirect('sponsor:listar')
    return render(request, "ajax/sponsor_confirmar_change.html", {"sponsor": query})

@login_required
@permission_required('sponsor.change_sucursal')
def ChangeStateSucursal(request,pk):
    query = Sucursal.objects.get(id=pk)
    if request.POST:
        if query.activo==0:
            query.activo=1
            messages.success(request, "Sucursal "+query.nombre +" habilitado.")
            query.save()
            return redirect('sponsor:listarSucursal')
        elif query.activo==1:
            query.activo=0
            messages.success(request, "Sucursal "+query.nombre +" deshabilitado.")
            query.save()
            return redirect('sponsor:listarSucursal')
    return render(request, "ajax/sucursal_confirmar_change.html", {"sucursal": query})