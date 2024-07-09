import json
from django.contrib.auth.mixins import LoginRequiredMixin
from seguridad.views import UsuarioPermissionRequieredMixin
from django.db.models import Sum
from django.db import DatabaseError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView
from novagym.utils import calculate_pages_to_render
from productos.filters import CategoriaFilter, ProductoFilter, UsuarioFilter
from productos.forms import *
from seguridad.models import UserDetails
from .serializers import *
from django.contrib import messages
from .models import *
import datetime
from sponsor.models import Sponsor
from novagym.models import TipoPago, Transaccion
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

@login_required
@permission_required('productos.add_categoria')
def createCategoria(request):
    if request.method=='POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createCategoria")
    else:
        form=CategoriaForm()
    return render(request,'createCategoria.html',{'form':form})

@login_required
@permission_required('productos.add_producto')
def createProducto(request):
    if request.method=='POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createProducto")
    else:
        form=ProductoForm()
    return render(request,'createProducto.html',{'form':form})

@login_required
@permission_required('productos.add_inventario')
def createInventario(request):
    if request.method=='POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createInventario")
    else:
        form=InventarioForm()
    return render(request,'createInventario.html',{'form':form})

@login_required
@permission_required('productos.add_descuento')
def createDescuento(request):
    if request.method=='POST':
        form = DescuentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createDescuento")
    else:
        form=DescuentoForm()
    return render(request,'createDescuento.html',{'form':form})


class crearCategoria(LoginRequiredMixin, UsuarioPermissionRequieredMixin,CreateView):
    form_class =CategoriaForm
    model=Categoria
    template_name = 'categoria_nueva.html'
    title = "CREAR CATEGORIA"
    success_url = reverse_lazy('productos:listarCategoria')
    permission_required = 'productos.add_categoria'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Agregar Categoría"
        return context

class editarCategoria(LoginRequiredMixin, UsuarioPermissionRequieredMixin,UpdateView):
    form_class =CategoriaForm
    model=Categoria
    template_name = 'categoria_nueva.html'
    title = "EDITAR CATEGORIA"
    permission_required = 'productos.change_categoria'
    success_url = reverse_lazy('productos:listarCategoria')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Categoría"
        return context

class ListarCategoria(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Categoria
    context_object_name = 'categoria'
    template_name = "lista_categoria.html"
    permission_required = 'novagym.view_empleado'
    permission_required = 'productos.view_categoria'
    filterset_class=CategoriaFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Categorias"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ListarProductos(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Producto
    context_object_name = 'producto'
    template_name = "lista_productos.html"
    permission_required = 'productos.view_producto'
    filterset_class=ProductoFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Productos"
        page_obj = context["page_obj"]
        context["total"]=Producto.objects.count()
        context["usanNovacoins"]=Producto.objects.filter(usaNovacoins=True).count()
        context["usaDolares"]=Producto.objects.filter(usaNovacoins=False).count()
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@login_required
@permission_required('productos.delete_categoria')
def deleteCategoria(request,id):
    query = Categoria.objects.get(id=id)
    if request.POST:
        try:
            query.delete()
        except:
            messages.error(request, "Imposible eliminar. Existen productos pertenecientes a la categoría")
            return redirect('productos:listarCategoria')
        messages.success(request, "Categoria eliminada con éxito.")
        return redirect('productos:listarCategoria')
    return render(request, "ajax/categoria_confirmar_elminar.html", {"categoria": query})

class CrearProducto(LoginRequiredMixin, UsuarioPermissionRequieredMixin,CreateView):
    form_class =ProductoForm
    template_name = 'producto_nuevo.html'
    title = "CREAR PRODUCTO"
    permission_required = 'productos.add_producto'
    def get_context_data(self, **kwargs):
        context = super(CrearProducto, self).get_context_data(**kwargs)
        context['title'] = "Agregar Producto"
        context['product_meta_formset'] = ProductoMeta()
        context['descuento_meta_formset'] = DescuentoMeta()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        product_meta_formset = ProductoMeta(self.request.POST)
        descuento_meta_formset = DescuentoMeta(self.request.POST)
        if form.is_valid() and product_meta_formset.is_valid() and descuento_meta_formset.is_valid():
            return self.form_valid(form, product_meta_formset,descuento_meta_formset)
        else:
            return self.form_invalid(form, product_meta_formset)

    def form_valid(self, form, product_meta_formset,descuento_meta_formset):
        self.object = form.save(commit=False)
        self.object.save()
        # saving ProductMeta Instances
        product_metas = product_meta_formset.save(commit=False)
        for meta in product_metas:
            meta.producto = self.object
            meta.save()
        descuento_metas = descuento_meta_formset.save(commit=False)
        for meta in descuento_metas:
            meta.producto = self.object
            meta.save()
        messages.success(self.request, "Producto creado con éxito!")
        return redirect(reverse("productos:listarProductos"))
    def form_invalid(self, form, product_meta_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                product_meta_formset=product_meta_formset
                                )
        )
class UpdateProducto(UpdateView):
    template_name = "producto_nuevo.html"
    model = Producto
    form_class = ProductoForm
    context_object_name = "first_obj"
    permission_required = 'productos.change_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Producto"
        if self.request.method == 'POST':
            context['product_meta_formset'] = ProductoMetaU(self.request.POST,instance=self.object)
            context['descuento_meta_formset'] = DescuentoMetaU(self.request.POST,instance=self.object)
        else:
            context['product_meta_formset'] = ProductoMetaU(instance=self.object)
            context['descuento_meta_formset'] = DescuentoMetaU(instance=self.object)
        return context

    def forms_valid(self, first, seconds,third):
        try:
            seconds.save()
            third.save()
            first.save()
            messages.success(self.request, "Actualización exitosa!")

        except DatabaseError as err:
            messages.error(self.request, "Ooops!  Algo salio mal...")
        return redirect(reverse("productos:listarProductos"))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        first_form = self.get_form(form_class)
        second_forms = ProductoMetaU(self.request.POST,instance=self.object)
        third_forms = DescuentoMetaU(self.request.POST,instance=self.object)
        if first_form.is_valid() and second_forms.is_valid() and third_forms.is_valid():
            return self.forms_valid(first_form , second_forms,third_forms)
        else:
            messages.error(self.request, "Ooops! Algo salio mal...")
            return redirect(reverse("productos:listarProductos"))


class Reportes(LoginRequiredMixin, UsuarioPermissionRequieredMixin,FilterView):
    template_name="reportes.html"
    model=User
    context_object_name = 'users'
    permission_required = 'seguridad.view_user'
    filterset_class=UsuarioFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Reportes de productos"
        context['list_url']=reverse_lazy('productos:reportes')
        return context

@login_required
@permission_required('productos.delete_producto')
def deleteProducto(request,id):
    producto = Producto.objects.get(id=id)
    inventario = Inventario.objects.get(producto_id=id)
    descuento = ProductoDescuento.objects.get(producto_id=id)
    if request.POST:
        descuento.delete()
        inventario.delete()
        producto.imagen.delete()
        producto.delete()
        messages.success(request, "Producto eliminado con éxito.")
        return redirect('productos:listarProductos')
    return render(request, "ajax/producto_confirmar_elminar.html", {"producto": producto})


def getAllProducts(request):
    urls={}
    productos=Inventario.objects.all()
    for producto in productos:
        id=producto.id
        descuento=0
        try:
            descuento = ProductoDescuento.objects.get(producto_id=producto.id)
        except ProductoDescuento.DoesNotExist:
            descuento = 0  # Handle the case where no ProductoDescuento exists
        urls[producto.producto.nombre]={
                            "id":producto.producto.id,
                            "codigo":producto.producto.codigo,
                            "descripcion":producto.producto.descripcion,
                            "imagen":request.build_absolute_uri('/media/')+str(producto.producto.imagen),
                            "categoria":str(producto.producto.categoria),
                            "talla":str(producto.producto.talla),
                            "precio":float(producto.precio),
                            "stock":producto.stock,
                            "novacoins":producto.novacoins,
                            "usaNovacoins":producto.producto.usaNovacoins,
                            "envio":producto.producto.envio,
                            "porcentajeDescuento": str(descuento.porcentaje_descuento) + "%" if descuento else "0%",
                            "fechaHoraDesde": str(descuento.fecha_hora_desde) if descuento else str(datetime.datetime.now()),
                            "fechaHoraHasta": str(descuento.fecha_hora_hasta) if descuento else str(datetime.datetime.now()),
                            "descuentoActivo": descuento.estado if descuento else False
                            }
    return HttpResponse(json.dumps(urls))

def all(request):
    query=Transaccion.objects.all()
    items=query.values()

    listItems=list(items)
    for i in listItems:
        userId=i["usuario_id"]
        pagoId=i["tipo_pago_id"]
        i["created_at"]=i["created_at"].replace(tzinfo=None).strftime("%d/%m/%Y %H:%M")
        usuario=UserDetails.objects.get(id=userId)
        pago=TipoPago.objects.get(id=pagoId)
        i["usuario_id"]=usuario.nombres + " " + usuario.apellidos
        i["tipo_pago_id"]=pago.nombre
    try:
        subtotal=query.aggregate(Sum("subtotal")).get("subtotal__sum")
        iva=query.aggregate(Sum("iva")).get("iva__sum")
        total=query.aggregate(Sum("valor_total")).get("valor_total__sum")
        response = {
            'items':listItems,
            'totales':{"subtotal":subtotal,
                        "iva":iva,
                        "total":total
                        }
        }
    except:
        response = {
            'items':listItems,
            'totales':{"subtotal":0,
                        "iva":0,
                        "total":0
                        }
        }
    return JsonResponse(response)

def dateRangeFilter(request):
    rango=request.GET.get("daterange", None)
    token=str(rango).split("-")
    fechaI=datetime.datetime.strptime(token[0].strip(" "), "%m/%d/%Y")
    fechaF=datetime.datetime.strptime(token[1].strip(" "), "%m/%d/%Y")

    query=Transaccion.objects.filter(created_at__range=(fechaI,fechaF))
    items=query.values()
    listItems=list(items)
    for i in listItems:
        userId=i["usuario_id"]
        pagoId=i["tipo_pago_id"]
        i["created_at"]=i["created_at"].replace(tzinfo=None).strftime("%d/%m/%Y %H:%M")
        usuario=UserDetails.objects.get(id=userId)
        pago=TipoPago.objects.get(id=pagoId)
        i["usuario_id"]=usuario.nombres + " " + usuario.apellidos
        i["tipo_pago_id"]=pago.nombre
    try:
        subtotal=query.aggregate(Sum("subtotal")).get("subtotal__sum")
        iva=query.aggregate(Sum("iva")).get("iva__sum")
        total=query.aggregate(Sum("valor_total")).get("valor_total__sum")
        response = {
            'items':listItems,
            'totales':{"subtotal":subtotal,
                        "iva":iva,
                        "total":total
                        }
        }
    except:
        response = {
            'items':listItems,
            'totales':{"subtotal":0,
                        "iva":0,
                        "total":0
                        }
        }
    return JsonResponse(response)

def update_items(request):
    rango=request.GET.get("daterange", None)
    token=str(rango).split("-")
    fechaI=datetime.datetime.strptime(token[0].strip(" "), "%m/%d/%Y")
    fechaF=datetime.datetime.strptime(token[1].strip(" "), "%m/%d/%Y")
    items=Sponsor.objects.all().filter(fecha_inicio__range=[fechaI,fechaF])
    return render(request, 'ajax/tableBody.html', {'items':items})