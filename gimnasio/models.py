from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

class Gimnasio(models.Model):
    class Ciudad(models.TextChoices):
        Guayaquil = 'Guayaquil', 'Guayaquil'
        Durán = 'Durán', 'Durán'
        Samborondón = 'Samborondón', 'Samborondón'
        Quito = 'Quito', 'Quito'
        Cuenca = 'Cuenca', 'Cuenca'
        Manta = 'Manta', 'Manta'

    phone_regex = RegexValidator(regex=r'^(0)[1-9]{1}(\s){1}[0-9]{7}', message="Ingrese el número en el formato correcto: 04 1234567")
    mobile_regex = RegexValidator(regex=r'^(09)[0-9]{8}', message="Ingrese el número en el formato correcto: 091234567")
    id = models.AutoField(primary_key=True,unique=True)
    nombre = models.CharField(max_length=24,unique=True)
    imagen = models.ImageField(upload_to="gimnasios/", null=True, blank=True,default="images/no_image.png")
    telefono = models.CharField(validators=[phone_regex], max_length=10, blank=True,null=True)
    celular = models.CharField(validators=[mobile_regex], max_length=10, blank=False,null=True)
    ubicacion = models.CharField(max_length=40)
    horario_inicio = models.TimeField(blank=False,null=False)
    horario_fin = models.TimeField(blank=False,null=False)
    estado = models.BooleanField(default=True)
    ciudad = models.CharField(max_length=15, choices=Ciudad.choices)
    aforo = models.PositiveIntegerField(blank=False,null=False)
    capacidad=models.PositiveIntegerField(blank=False,null=False)
    personas= models.PositiveIntegerField(null=True, blank=True)
    latitud= models.DecimalField(decimal_places=5,max_digits=9,null=True, blank=True,)
    longitud= models.DecimalField(decimal_places=5,max_digits=9,null=True, blank=True,)
    class Meta:
        ordering=('-id',)
    def __str__(self):
        return self.nombre +"-"+self.ciudad