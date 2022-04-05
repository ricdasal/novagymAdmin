from django.db import models
from django.core.validators import RegexValidator
import sys
sys.path.append("..")
# Create your models here.
class Promociones(models.Model):  
    phone_regex = RegexValidator(regex=r'^(0)[1-9]{1}(\s){1}[0-9]{7}', message="Ingrese el número en el formato correcto: 04 1234567")
    mobile_regex = RegexValidator(regex=r'^(09)[0-9]{8}', message="Ingrese el número en el formato correcto: 091234567")

    id=models.AutoField(primary_key=True)
    titulo=models.CharField(max_length=30)
    descripcion=models.CharField(max_length=130)
    fecha_hora_inicio=models.DateTimeField()
    fecha_hora_fin=models.DateTimeField()
    imagen = models.ImageField(upload_to="promociones/", null=True, blank=True,default="images/no_image.png")
    telefono = models.CharField(validators=[phone_regex], max_length=10, blank=True,null=True)
    celular = models.CharField(validators=[mobile_regex], max_length=10, blank=True,null=True)
    nombre_contacto = models.CharField(max_length=24)
    url = models.URLField(max_length=50)
    correo=models.EmailField(max_length=50,blank=False,null=False)
    activo=models.BooleanField(default=True)