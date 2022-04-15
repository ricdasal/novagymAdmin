import sys

from novacoin.models import Cartera, DetalleCartera
from seguridad.models import UserDetails
sys.path.append("..")
from django.shortcuts import render
from productos.models import Categoria, Producto
from sponsor.models import Sponsor
from django.http import JsonResponse
import random as rd

def listar(request):
    categorias=Categoria.objects.all()
    return render(request, "lista_reportes.html", {"title":"REPORTES","categorias":categorias})

def listarNc(request):
    detalle=UserDetails.objects.all()
    return render(request, "lista_reportes_novacoins.html", {"title":"REPORTES NOVACOINS","detalle":detalle})

def grafico_detallescartera(request, id):
    #cartera=Cartera.objects.get(usuario_id=id)
    #productos=DetalleCartera.objects.filter(cartera_id=cartera.id)
    #name=Categoria.objects.get(id=id)
    detalles=UserDetails.objects.all()
    labels=[]
    data=[]

    return JsonResponse({
        'title': 'Registro de transacciones en NovaCoins',
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

def grafico_fechas(request, fechaI,fechaF):
    sponsors=Sponsor.objects.filter(fecha_inicio__range=[fechaI, fechaF])
    labels=[]
    data=[]
    for sponsor in sponsors:
        labels.append(sponsor.nombre)
        data.append(rd.randint(5,20))
    return JsonResponse({
        'title': f'Productos vendidos por los sponsors durante {fechaI} - {fechaF}',
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

