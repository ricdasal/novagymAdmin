from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import redirect, render
from django.shortcuts import render
from gimnasio.forms import GimnasioForm
from .serializers import *
from django.core.mail import send_mail

from .models import *

# Create your views here.
#Gimnasio - Contacto

@api_view(["GET"])
def gimnasioList(request):
    gimnasio= Gimnasio.objects.all()
    serializer=GimnasioSerializer(gimnasio,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def gimnasioDetail(request,id):
    gimnasio= Gimnasio.objects.get(id=id)
    serializer=GimnasioSerializer(gimnasio,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def gimnasioCreate(request):
    serializer=GimnasioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def gimnasioUpdate(request,id):
    gimnasio= Gimnasio.objects.get(id=id)
    serializer=GimnasioSerializer(instance=gimnasio,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def gimnasioDelete(request,id):
    gimnasio= Gimnasio.objects.get(id=id)
    try:
        gimnasio.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def createGimnasio(request):
    if request.method=='POST':
        form = GimnasioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gimnasio:createGimnasio")
    else:
        form=GimnasioForm()
    return render(request,'createGimnasio.html',{'form':form})