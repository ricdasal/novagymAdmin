from django.core.management.base import BaseCommand, CommandError
from cardauth.models import Cardauth
from membresia.models import Historial, Membresia
from novagym.models import DetalleTransaccionMembresia, Transaccion
from seguridad.models import UserDetails
import hashlib
import base64
import random
from datetime import datetime, timedelta
import json
import requests
from django.utils import timezone
from dateutil.relativedelta import relativedelta

URL_PAYMENT = "https://checkout-test.placetopay.ec/api/"

class Command(BaseCommand):
    help = 'Cobro de mensualidades si es que estas tienen activada el pago recurrente'

    def handle(self, *args, **options):
        login = "26baefb36e8855417722f6276cc03ec7"
        secretKey = "0C82nq53xEMd5Nz4"
        
        # Get current date-time as ISO string
        seed = (datetime.utcnow() + timedelta(minutes=5)).isoformat() + 'Z'

        # Generate random integer
        raw_nonce = random.randint(0, 1000000)

        # Get expiration time as ISO string
        expiration = (datetime.utcnow() + timedelta(minutes=30)).isoformat() + 'Z'

        # Convert rawNonce to bytes and encode as base64 string
        nonce_bytes = str(raw_nonce).encode('utf-8')
        nonce_base64 = base64.b64encode(nonce_bytes).decode('utf-8')

        # Combine rawNonce, seed, and secretKey
        combined_data = (str(raw_nonce) + seed + secretKey).encode('utf-8')

        # Hash combined data using SHA-256
        hashed_data = hashlib.sha256(combined_data).digest()

        # Encode hashed data as base64 string
        tran_key_base64 = base64.b64encode(hashed_data).decode('utf-8')

        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }

        self.cobro_recurrente(headers, login, tran_key_base64, nonce_base64, seed, expiration)

    def crear_transaccion(self, data):
        # Extraer datos de la transacción
        detalles_data = data.pop('transaccion_membresia')
        gimnasio = data.pop('gimnasio', None)
        pagoRecurrente = data.pop('pagoRecurrente', None)
        
        # Crear la transacción principal
        transaccion = Transaccion.objects.create(**data)
        
        # Crear detalles de la transacción
        for membresia_data in detalles_data:
            DetalleTransaccionMembresia.objects.create(
                transaccion=transaccion, **membresia_data)
        
        # Guardar la transacción principal
        transaccion.save()
        
        # Obtener la membresía del primer detalle
        membresia = transaccion.transaccion_membresia.all()[0].membresia
        fecha_inicio = timezone.now()
        
        # Obtener el usuario asociado a la transacción
        usuario = transaccion.usuario.detalles
        
        # Desactivar la membresía actual del usuario si existe
        if usuario.tiene_membresia:
            current_membresia = usuario.membresia
            current_membresia.activa = False
            current_membresia.save()
        
        # Crear una entrada en el historial de membresías
        Historial.objects.create(
            usuario=usuario,
            membresia=membresia,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_inicio + relativedelta(
                months=membresia.meses_duracion,
                days=membresia.dias_duracion),
            costo=membresia.precio,
            activa=True,
            gimnasio_id=gimnasio,
            pagoRecurrente=pagoRecurrente
        )

    def cobro_recurrente(self, headers, login, tran_key_base64, nonce_base64, seed, expiration):
        usuarios = UserDetails.objects.all()
        historialMembresias = Historial.objects.all()

        for usuario in usuarios:
            
            lista = historialMembresias.filter(usuario_id=usuario.id)
            tamanoLista = len(lista)
            
            
            if tamanoLista > 0:
                buyer = {
                    "name": f"{usuario.nombres} {usuario.apellidos}",
                    "email": usuario.usuario.email,
                    # Include other buyer details as needed
                }
                usuario_id = usuario.usuario.id
                try:
                    card = Cardauth.objects.get(usuario_id=usuario_id)
                    token = card.token
                    historial = lista[tamanoLista - 1]
                    membresia = Membresia.objects.get(id=historial.membresia.pk)
                except Cardauth.DoesNotExist:
                    print(f"No card found for user {usuario_id}")
                    continue
                
                if historial.fecha_fin < timezone.now():
                    print(historial.fecha_fin)
                else:
                    print(timezone.now())
                
                if historial.pagoRecurrente and historial.fecha_fin < timezone.now():
                    data = {
                        "locale": "es_CO",
                        "auth": {
                            "login": login,
                            "tranKey": tran_key_base64,
                            "nonce": nonce_base64,
                            "seed": seed,
                        },
                        "payment": {
                            "reference": "PAGO_MENSUAL",
                            "description": "PAGO DE ESTE MES",
                            "amount": {"currency": "USD", "total": historial.costo},
                        },
                        "payer": {
                            "document": card.payerDocument,
                            "documentType": card.payerDocumentType,
                            "name": card.payerName,
                            "surname": card.payerSurname,
                            "email": card.payerEmail,
                            "mobile": card.payerMobile
                        },
                        "instrument": {
                            "token": {
                                "token": token
                            }
                        },
                        "expiration": expiration,
                        "returnUrl": "https://dnetix.co/p2p/client",
                        "cancelUrl": "https://docs.placetopay.dev",
                        "ipAddress": "127.0.0.1",
                        "userAgent": "PlacetoPay",
                        "buyer": buyer,
                    }
                    print(data)
                    response = self.make_payment_request(data, headers)

                    transaccion_data = {
                        "usuario": usuario,
                        "subtotal": historial.costo,
                        "gimnasio": historial.gimnasio,
                        "membresia": membresia
                    }

                    if response:
                        transaccion = {
                            "nombre_user": data["usuario"].nombres + data["usuario"].apellidos,
                            "auth_code": "PAGO_APP",
                            "id_tramite": response['requestId'],
                            "subtotal": data["subtotal"],
                            "descuento": 0,
                            "iva": data["subtotal"] * 0.15,
                            "valor_total": data["subtotal"] * 1.15,
                            "gimnasio": data["gimnasio"],
                            "estado": "PAG",
                            "pagoRecurrente": True,
                            "transaccion_membresia": [
                                {
                                    "membresia": data["membresia"].id,
                                    "categoria": "Membresia",
                                    "descripcion": data["membresia"].descripcion,
                                    "cantidad": 1,
                                    "precio": data["membresia"].precio,
                                    "total": data["membresia"].precio        
                                }
                            ]  
                        }
                        self.crear_transaccion(transaccion)
                        #self.guardar_transaccion(transaccion_data, response['requestId'])
                        print("Requerimiento exitoso")
                    else:
                        print("Error en el requerimiento")

    def guardar_transaccion(self, data, id_tramite):
         # Asegúrate de definir esto correctamente
        
        transaccion = {
            "nombre_user": data["usuario"].nombres + data["usuario"].apellidos,
            "auth_code": "PAGO_APP",
            "id_tramite": id_tramite,
            "subtotal": data["subtotal"],
            "descuento": 0,
            "iva": data["subtotal"] * 0.15,
            "valor_total": data["subtotal"] * 1.15,
            "gimnasio": data["gimnasio"],
            "estado": "PAG",
            "pagoRecurrente": True,
            "transaccion_membresia": [
                {
                    "membresia": data["membresia"].id,
                    "categoria": "Membresia",
                    "descripcion": data["membresia"].descripcion,
                    "cantidad": 1,
                    "precio": data["membresia"].precio,
                    "total": data["membresia"].precio        
                }
            ]  
        }
        self.crear_transaccion(transaccion)

    def make_payment_request(self, data, headers):
        try:
            response = requests.post(URL_PAYMENT + "collect", json=data, headers=headers)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en el requerimiento: {e}")
            return None