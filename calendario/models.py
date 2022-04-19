import random
from django.db import models
from seguridad.models import UserDetails
from gimnasio.models import Gimnasio

# Create your models here.

def generarCodigo():
    not_unique = True
    while not_unique:
        unique_code = random.randint(0, 999999)
        codeString=str(unique_code).zfill(6)
        if not MaquinaReserva.objects.filter(codigo=codeString):
            not_unique = False
            return codeString

def generarCodigoMaquina():
    not_unique = True
    while not_unique:
        unique_code = "MCN-"+str(random.randint(1000, 9999))
        if not MaquinaReserva.objects.filter(codigo=unique_code):
            not_unique = False
            return str(unique_code)


class Zona(models.Model):
    class Tipo(models.TextChoices):
        MAQUINA = 'maquinas', 'Máquinas'
        CLASES = 'clases', 'Clases'
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=24)
    espacios=models.PositiveIntegerField(max_length=2)
    tipo=models.CharField(max_length=10,choices=Tipo.choices)
    class Meta:
        ordering=('-id',)
    def __str__(self):
        return self.nombre+"-"+self.tipo

class Horario(models.Model):
    id = models.AutoField(primary_key=True)
    class Dia(models.TextChoices):
        LUNES = 'LUNES', 'LUNES'
        MARTES = 'MARTES', 'MARTES'
        MIERCOLES = 'MIERCOLES', 'MIERCOLES'
        JUEVES = 'JUEVES', 'JUEVES'
        VIERNES = 'VIERNES', 'VIERNES'
        SABADO = 'SABADO', 'SABADO'
        DOMINGO = 'DOMINGO', 'DOMINGO'
    dia=models.CharField(max_length=10, choices=Dia.choices)
    nombre = models.CharField(max_length=24)
    descripcion = models.CharField(max_length=255)
    horario_inicio = models.TimeField(blank=False)
    horario_fin = models.TimeField(blank=False)
    gimnasio=models.ForeignKey(Gimnasio, on_delete=models.PROTECT)
    capacidad=models.PositiveIntegerField(max_length=2)
    asistentes=models.PositiveIntegerField(max_length=2,default=0)
    activo=models.BooleanField(default=True)
    zona=models.ForeignKey(Zona,on_delete=models.PROTECT)
    class Meta:
        ordering=('horario_inicio',)
    def __str__(self):
        return self.nombre



class Maquina(models.Model):
    class Categoria(models.TextChoices):
        CORRER = 'Cintas de correr', 'Cintas de correr'
        BICICLETAS = 'Bicicletas', 'Bicicletas'
        ELIPTICAS = 'Elipticas', 'Elipticas'
        REMO = 'Remo', 'Remo'
        FUERZA = 'Fuerza', 'Fuerza'
        HERRAMIENTAS = 'Herramientas', 'Herramientas'
    codigo=codigo=models.CharField(max_length=20, unique=True, default=generarCodigoMaquina, editable=False)
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=24)
    descripcion = models.CharField(max_length=255)
    imagen=models.ImageField(upload_to="maquinas/", null=False, blank=False,default="images/no_image.png")
    categoria=models.CharField(max_length=20, choices=Categoria.choices)  
    cantidad=models.PositiveIntegerField(max_length=2)
    reservable=models.BooleanField(default=True,null=False, blank=False)
    activo=models.BooleanField(default=True,null=False, blank=False)
    zona=models.ForeignKey(Zona, on_delete=models.PROTECT)

class Posicion(models.Model):
    id=models.AutoField(primary_key=True)
    posicion=models.PositiveIntegerField(max_length=2)
    zona=models.ForeignKey(Zona, on_delete=models.CASCADE)
    ocupado=models.BooleanField(default=False)
    def __str__(self):
        return str(self.zona)+"-"+str(self.posicion)+"-"+str(self.ocupado)

class PosicionMaquina(models.Model):
    id=models.AutoField(primary_key=True)
    fila=models.CharField(max_length=2)
    columna=models.PositiveIntegerField(max_length=2)
    ocupado=models.BooleanField(default=False)
    maquina=models.ForeignKey(Maquina, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.maquina)+"-"+str(self.fila)+str(self.columna)

class MaquinaReserva(models.Model):
    id=models.AutoField(primary_key=True)
    codigo=models.CharField(max_length=20, unique=True, default=generarCodigo, editable=False)
    maquina=models.ForeignKey(Maquina,on_delete=models.PROTECT)
    horario_inicio=models.TimeField()
    horario_fin=models.TimeField
    posicion=models.ForeignKey(PosicionMaquina, on_delete=models.PROTECT)
    usuario=models.ForeignKey(UserDetails,on_delete=models.PROTECT)
    fecha= models.DateTimeField(auto_now_add=True)

class HorarioReserva(models.Model):
    id = models.AutoField(primary_key=True)
    codigo=models.CharField(max_length=20, unique=True, default=generarCodigo, editable=False)
    horario=models.ForeignKey(Horario,on_delete=models.PROTECT)
    usuario=models.ForeignKey(UserDetails,on_delete=models.PROTECT)
    posicion=models.ForeignKey(Posicion, on_delete=models.PROTECT, blank=True,null=True)
    fecha= models.DateTimeField(auto_now_add=True)