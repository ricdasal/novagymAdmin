from django.shortcuts import redirect, render
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .forms import *
from .serializers import *
from django.core.mail import send_mail

from .models import *

# Create your views here.
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

def createSponsor(request):
    if request.method=='POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sponsor:createSponsor")
    else:
        form=SponsorForm()
    return render(request,'createSponsor.html',{'form':form})