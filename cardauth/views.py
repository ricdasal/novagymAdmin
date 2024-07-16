from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
import json
from .models import Cardauth 
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User





# Create your views here.

#aqui es donde se añade una credencial mediante mysql
# @csrf_exempt
# def addCodigoAuth(request):
#     if request.method == 'POST':
#         response = json.loads(request.body)
#         print(response)
#         ntoken=response["token"]
#         nauth=response["cvc"]

#         try:
#             existe = Cardauth.objects.filter(token= ntoken)
#             total = existe.count()
#             if total == 0:
#                 ncard = Cardauth(token=ntoken,auth=nauth)
#                 ncard.save()
#                 response_data = {
#                     'valid': 'OK'
#                 }
#                 return JsonResponse(response_data,safe=False)
#         except Cardauth.DoesNotExist:
#             ncard = Cardauth(token=ntoken,auth=nauth)
#             ncard.save()
#             response_data = {
#                 'valid': 'OK'
#             }
#             return JsonResponse(response_data,safe=False)
    
#     response_data = {
#         'valid': 'NO'
#     }
#     return JsonResponse(response_data,safe=False)

@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addCodigoAuth(request):
    if request.method == 'POST':
        # Parse JSON data from request body
        try:
            data = json.loads(request.body)
            nusuario = data["usuario_id"]
            ntoken = data["token"]
            nsubtoken = data["subtoken"]
            nlast_digits = data["lastDigits"]
            npayerDocument = data["payerDocument"]
            npayerDocumentType = data["payerDocumentType"]
            npayerName = data["payerName"]
            npayerSurname = data["payerSurname"]
            npayerEmail = data["payerEmail"]
            npayerMobile = data["payerMobile"]

            # Get User instance
            n_usuario = User.objects.get(id=nusuario)


            # Check if token already exists
            exists = Cardauth.objects.filter(token=ntoken).exists()
            if not exists:
                # Create a new Cardauth instance
                new_cardauth = Cardauth(
                    usuario=n_usuario,
                    token=ntoken,
                    subtoken=nsubtoken,
                    lastDigits=nlast_digits,
                    payerDocument=npayerDocument,
                    payerDocumentType=npayerDocumentType,
                    payerName=npayerName,
                    payerSurname=npayerSurname,
                    payerEmail=npayerEmail,
                    payerMobile=npayerMobile,
                )
                new_cardauth.save()

                response_data = {
                    'valid': 'OK'
                }
                return JsonResponse(response_data)
            else:
                response_data = {
                    'valid': 'Token already exists'
                }
                return JsonResponse(response_data, status=400)

        except KeyError:
            response_data = {
                'valid': 'Missing required fields'
            }
            return JsonResponse(response_data, status=400)

        except json.JSONDecodeError:
            response_data = {
                'valid': 'Invalid JSON'
            }
            return JsonResponse(response_data, status=400)

    response_data = {
        'valid': 'NO'
    }
    return JsonResponse(response_data)
# aqui es donde se busca una credencial por token mediane mysql
# @csrf_exempt
# def getCodigoAuth(request):
#     if request.method == 'GET':
#         valor = request.GET.get("token")
#         print(valor)
#         if valor!= None:
#             cards = Cardauth.objects.get(token=valor)
#             return JsonResponse(cards.auth,safe=False)
#     return HttpResponse(status=400)

@csrf_exempt
def getCodigoAuth(request):
    if request.method == 'GET':
        usuario_id = request.GET.get("usuario_id")
        if usuario_id:
            try:
                cards = Cardauth.objects.filter(usuario_id=usuario_id)
                data = list(cards.values("token", "subtoken", "auth", "lastDigits"))
                return JsonResponse(data, safe=False)
            except Cardauth.DoesNotExist:
                return JsonResponse({"error": "No Cardauth found for the user"}, status=404)
        else:
            return HttpResponse("Parameter 'usuario_id' is required.", status=400)

    return HttpResponse(status=400)

# aqui es donde se elimina una credencial por token
@csrf_exempt
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

