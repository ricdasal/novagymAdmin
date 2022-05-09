from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import  ListView
from novagym.utils import calculate_pages_to_render
from seguridad.views import UsuarioPermissionRequieredMixin
from rest_framework import viewsets
from .models import Transaccion, DetalleTransaccion
from django.contrib import messages
import requests
import json
import time
import hashlib
from base64 import b64encode

def AnularTransaccion(request, id):
    print("estoy aqui en anular")
    data = Transaccion.objects.get(id=id)
    return render(request, "ajax/transaccion_delete.html", {"data": data})

def showDetalleTransaccion(request, id):
    detalles = DetalleTransaccion.objects.all().filter(transaccion=id)
    return render(request, "ajax/detalles.html", {"detalles": detalles})

def PaymentezRefound(request, id):
    tran = Transaccion.objects.get(id=id)
    if request.POST:
        tran.estado = 'CNC'
        tran.save()
        url = 'https://ccapi-stg.paymentez.com/v2/transaction/refund/'
        transaction = {
            "transaction": {
                "id": tran.id_tramite
            }
        }
        headers = {
            'Content-Type': 'application/json',
            'Auth-Token': authToken('TPP3-EC-SERVER','JdXTDl2d0o0B8ANZ1heJOq7tf62PC6')
        }
        r = requests.post(url, data=json.dumps(transaction), headers=headers)
        messages.success(request, "Transaccion anulada Correctamente")
        return redirect('transacciones:listar')
    return redirect('transacciones:listar')

def  authToken(paymentez_server_application_code,paymentez_server_app_key):
    unix_timestamp = str(int(time.time()))
    uniq_token_string = paymentez_server_app_key + unix_timestamp
    uniq_token_hash = hashlib.sha256(
        uniq_token_string.encode('utf-8')).hexdigest()
    auth_token = b64encode(bytes('%s;%s;%s' % (paymentez_server_application_code,
                                               unix_timestamp, uniq_token_hash), 'utf-8'))
    return auth_token

class ListarTransaccion(LoginRequiredMixin, UsuarioPermissionRequieredMixin, ListView):
    paginate_by = 20
    max_pages_render = 10
    model = Transaccion
    context_object_name = 'transacciones'
    template_name = "listar_transacciones.html"
    permission_required = 'transacciones.view_transaccion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Transacciones"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context
