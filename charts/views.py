import sys

from productos.filters import ProductoFilter
sys.path.append("..")
from django.shortcuts import render
from productos.models import Categoria, Producto
from django.http import JsonResponse
from django.core import serializers
from django_filters.views import FilterView
from django.views.decorators.http import require_http_methods


def listar(request):
    categorias=Categoria.objects.all()

    return render(request, "lista_reportes.html", {"title":"REPORTES","categorias":categorias})

def grafico_categorias(request, id):
    productos=Producto.objects.filter(categoria=id).order_by("nombre")
    name=Categoria.objects.get(id=id)
    labels=[]
    data=[]
    for producto in productos:
        labels.append(producto.nombre)
        inventario = producto.inventario_set.all()
        data.append(inventario[0].stock)

    return JsonResponse({
        'title': f'Stock para los productos de la categoria: {name}',
        'data': {
            'labels': labels,
            
            'datasets': [{
                'label': 'Unidades',
                'backgroundColor': "blue",
                'borderColor': "black",
                'data': data,
            }]
        },
    })

def productos_chart(request):
    labels = []
    data = []
    
    queryset = Producto.objects.all()
    for entry in queryset:
        inventario = entry.inventario_set.all()
        labels.append(entry.nombre)
        data.append(inventario[0].stock)
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

""" def postFriend(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = FriendForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400) """