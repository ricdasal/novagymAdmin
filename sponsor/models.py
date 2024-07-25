import random
from django import forms
from django.db import models
from datetime import date, datetime
from django.core.validators import RegexValidator
# Create your models here.

def generarCodigo():
    not_unique = True
    while not_unique:
        unique_code = "SPR-"+str(random.randint(1000, 9999))
        if not Sponsor.objects.filter(codigo=unique_code):
            not_unique = False
            return str(unique_code)

def generarCodigoS():
    not_unique = True
    while not_unique:
        unique_code = "SUC-"+str(random.randint(1000, 9999))
        if not Sucursal.objects.filter(codigo=unique_code):
            not_unique = False
            return str(unique_code)

class Sponsor(models.Model):
    phone_regex = RegexValidator(regex=r'^(0)[1-9]{1}(\s){1}[0-9]{7}', message="Ingrese el número en el formato correcto: 04 1234567")
    mobile_regex = RegexValidator(regex=r'^(09)[0-9]{8}', message="Ingrese el número en el formato correcto: 091234567")
    red_regex=RegexValidator(regex=r'((,)?\b(instagram|facebook|twitter|tiktok|youtube)\b:[a-zA-Z-1-9-@\.-_]+)+', message="Ingrese las redes sociales separadas por comas sin espacios")
    #red_regex=RegexValidator(regex=r'([a-zA-Z-1-9-@\.-_]+(,)?)+', message="Ingrese las redes sociales separadas por comas sin espacios")

    id = models.AutoField(primary_key=True,unique=True)
    codigo = models.CharField(max_length=20,unique=True,default=generarCodigo,editable=False)
    nombre = models.CharField(max_length=24)
    descripcion = models.CharField(max_length=255)
    direccion=models.CharField(max_length=70,blank=False,null=False)
    telefono = models.CharField(validators=[phone_regex], max_length=10, blank=True,null=True)
    celular = models.CharField(validators=[mobile_regex], max_length=10, blank=False,null=True)
    nombre_contacto = models.CharField(max_length=24)
    url = models.URLField(max_length=50)
    red_social = models.CharField(validators=[red_regex],max_length=255,blank=True,null=True)
    imagen = models.ImageField(upload_to="anunciantes/", null=False, blank=False,default="images/no_image.png")
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    activo=models.BooleanField(default=True)
    horario_apertura=models.TimeField()
    horario_cierre=models.TimeField()
    es_matriz=models.BooleanField(default=True)
    correo=models.EmailField(max_length=50,blank=False,null=False)
    beneficios=models.CharField(max_length=500)
    class Meta:
        ordering=('-id',)
    def __str__(self):
        return str(self.nombre)
    def listaRedes(self):
        redes=self.red_social.split(',')
        lista={}
        for red in redes:
            token=red.split(":")
            lista[token[0]]=token[1]
        return lista

    @property
    def compararFechas(self):
        if ((self.fecha_inicio <= date.today() <= self.fecha_fin) and (self.fecha_inicio <= self.fecha_fin)) or date.today() < self.fecha_fin:
            return True
        else:
            return False


class Sucursal(models.Model):
    phone_regex = RegexValidator(regex=r'^(0)[1-9]{1}(\s){1}[0-9]{7}', message="Ingrese el número en el formato correcto: 04 1234567")
    mobile_regex = RegexValidator(regex=r'^(09)[0-9]{8}', message="Ingrese el número en el formato correcto: 091234567")
    id = models.AutoField(primary_key=True,unique=True)
    codigo = models.CharField(max_length=20,unique=True,default=generarCodigoS,editable=False)
    direccion=models.CharField(max_length=70,blank=False,null=False)
    nombre = models.CharField(max_length=24)
    telefono = models.CharField(validators=[phone_regex], max_length=10, blank=True,null=True)
    celular = models.CharField(validators=[mobile_regex], max_length=10, blank=False,null=True)
    imagen = models.ImageField(upload_to="sucursales/", null=True, blank=True,default="images/no_image.png")
    horario_apertura=models.TimeField()
    horario_cierre=models.TimeField()
    sponsor=models.ForeignKey(Sponsor,on_delete=models.CASCADE)
    correo=models.EmailField(max_length=50,blank=True,null=True)
    activo=models.BooleanField(default=True)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    class Meta:
        ordering=('-id',)
    def __str__(self):
        return str(self.nombre)