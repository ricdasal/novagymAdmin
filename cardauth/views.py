from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
import json
from .models import Cardauth


# Create your views here.

#aqui es donde se añade una credencial mediante mysql
def addCodigoAuth(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        print(response)
        ntoken=response["token"]
        nauth=response["cvc"]

        try:
            existe = Cardauth.objects.filter(token= ntoken)
            total = existe.count()
            if total == 0:
                ncard = Cardauth(token=ntoken,auth=nauth)
                ncard.save()
                response_data = {
                    'valid': 'OK'
                }
                return JsonResponse(response_data,safe=False)
        except Cardauth.DoesNotExist:
            ncard = Cardauth(token=ntoken,auth=nauth)
            ncard.save()
            response_data = {
                'valid': 'OK'
            }
            return JsonResponse(response_data,safe=False)
    
    response_data = {
        'valid': 'NO'
    }
    return JsonResponse(response_data,safe=False)

# aqui es donde se busca una credencial por token mediane mysql
def getCodigoAuth(request):
    if request.method == 'GET':
        valor = request.GET.get("token")
        print(valor)
        if valor!= None:
            cards = Cardauth.objects.get(token=valor)
            return JsonResponse(cards.auth,safe=False)
    return HttpResponse(status=400)

# aqui es donde se elimina una credencial por token
def delCodigoAuth(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        ntoken = response["token"]
        print(ntoken)

        try:
            record = Cardauth.objects.filter(token=ntoken)
            record.delete()
            response_data = {
                'valid': 'OK'
            }
            return JsonResponse(response_data,safe=False)
        except:
            response_data = {
                'valid': 'NO'
            }
            return JsonResponse(response_data,safe=False)
    response_data = {
        'valid': 'NO'
    }
    return JsonResponse(response_data,safe=False)


