import random
from django import forms
from django.db import models
from datetime import date, datetime
from django.core.validators import RegexValidator
# Create your models here.

def generarCodigo():
    not_unique = True
    while not_unique:
        unique_code = random.randint(1000, 9999)
        if not Sponsor.objects.filter(codigo=unique_code):
            not_unique = False
            return "SPR"+"-"+str(unique_code)

class Sponsor(models.Model):
    phone_regex = RegexValidator(regex=r'^(09)[0-9]{8}', message="Ingrese el número en el formato correcto: 091234567")

    id = models.AutoField(primary_key=True,unique=True)
    codigo = models.CharField(max_length=20,unique=True,default=generarCodigo,editable=False)
    nombre = models.CharField(max_length=24)
    descripcion = models.CharField(max_length=255)
    telefono = models.CharField(validators=[phone_regex], max_length=10, blank=True)
    nombre_contacto = models.CharField(max_length=24)
    url = models.URLField(max_length=50)
    imagen = models.ImageField(upload_to="anunciantes/", null=False, blank=False,default="images/no_image.png")
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    activo=models.BooleanField(default=True)

    def __str__(self):
        return str(self.nombre)

    @property
    def compararFechas(self):
        if ((self.fecha_inicio <= date.today() <= self.fecha_fin) and (self.fecha_inicio <= self.fecha_fin)) or date.today() < self.fecha_fin:
            return True
        else:
            return False
