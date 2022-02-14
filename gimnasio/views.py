from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
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
