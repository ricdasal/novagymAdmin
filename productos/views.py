from django.shortcuts import redirect, render
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from productos.forms import *
from .serializers import *
from django.core.mail import send_mail

from .models import *
# Create your views here.
#Send email
def enviarCorreo(request):
    if request.method=="POST":
        titulo=request.POST["titulo"]
        receptor=request.POST["receptor"]
        mensaje=request.POST["mensaje"]
        send_mail(titulo,mensaje,receptor,["admin@novagym.com"])
        return render(request,"template.html",{})
#SPONSOR

@api_view(["GET"])
def sponsorList(request):
    sponsors= Sponsor.objects.all()
    serializer=SponsorSerializer(sponsors,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def sponsorDetail(request,id):
    sponsors= Sponsor.objects.get(id=id)
    serializer=SponsorSerializer(sponsors,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def sponsorCreate(request):
    serializer=SponsorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def sponsorUpdate(request,id):
    sponsor= Sponsor.objects.get(id=id)
    serializer=SponsorSerializer(instance=sponsor,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def sponsorDelete(request,id):
    sponsor= Sponsor.objects.get(id=id)
    try:
        sponsor.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#PRODUCTO

@api_view(["GET"])
def productoList(request):
    producto= Producto.objects.all()
    serializer=ProductoSerializer(producto,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def productoDetail(request,id):
    producto= Producto.objects.get(id=id)
    serializer=ProductoSerializer(producto,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def productoCreate(request):
    serializer=ProductoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def productoUpdate(request,id):
    producto= Producto.objects.get(id=id)
    serializer=ProductoSerializer(instance=producto,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def productoDelete(request,id):
    producto= Producto.objects.get(id=id)
    try:
        producto.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Categoria

@api_view(["GET"])
def categoriaList(request):
    categoria= Categoria.objects.all()
    serializer=CategoriaSerializer(categoria,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def categoriaDetail(request,id):
    categoria= Categoria.objects.get(id=id)
    serializer=CategoriaSerializer(categoria,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def categoriaCreate(request):
    serializer=CategoriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def categoriaUpdate(request,id):
    categoria= Categoria.objects.get(id=id)
    serializer=CategoriaSerializer(instance=categoria,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def categoriaDelete(request,id):
    categoria= Categoria.objects.get(id=id)
    try:
        categoria.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Inventario

@api_view(["GET"])
def inventarioList(request):
    inventario= Inventario.objects.all()
    serializer=InventarioSerializer(inventario,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def inventarioDetail(request,id):
    inventario= Inventario.objects.get(id=id)
    serializer=InventarioSerializer(inventario,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def inventarioCreate(request):
    serializer=InventarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def inventarioUpdate(request,id):
    inventario= Inventario.objects.get(id=id)
    serializer=InventarioSerializer(instance=inventario,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def inventarioDelete(request,id):
    inventario= Inventario.objects.get(id=id)
    try:
        inventario.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#ProductoDescuento

@api_view(["GET"])
def descuentoList(request):
    descuento= ProductoDescuento.objects.all()
    serializer=ProductoDescuentoSerializer(descuento,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def descuentoDetail(request,id):
    descuento= ProductoDescuento.objects.get(id=id)
    serializer=ProductoDescuentoSerializer(descuento,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def descuentoCreate(request):
    serializer=ProductoDescuentoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def descuentoUpdate(request,id):
    descuento= ProductoDescuento.objects.get(id=id)
    serializer=ProductoDescuentoSerializer(instance=descuento,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def descuentoDelete(request,id):
    descuento= ProductoDescuento.objects.get(id=id)
    try:
        descuento.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def createCategoria(request):
    if request.method=='POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createCategoria")
    else:
        form=CategoriaForm()
    return render(request,'createCategoria.html',{'form':form})

def createProducto(request):
    if request.method=='POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createProducto")
    else:
        form=ProductoForm()
    return render(request,'createProducto.html',{'form':form})

def createInventario(request):
    if request.method=='POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createInventario")
    else:
        form=InventarioForm()
    return render(request,'createInventario.html',{'form':form})


def createDescuento(request):
    if request.method=='POST':
        form = DescuentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createDescuento")
    else:
        form=DescuentoForm()
    return render(request,'createDescuento.html',{'form':form})