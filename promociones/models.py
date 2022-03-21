from django.db import models
from productos.models import Categoria
from membresia.models import Membresia
import sys
sys.path.append("..")
# Create your models here.
class Promociones(models.Model):
    id=models.AutoField(primary_key=True)
    titulo=models.CharField(max_length=30)
    fecha_hora_inicio=models.DateTimeField()
    fecha_hora_fin=models.DateTimeField()
    imagen = models.ImageField(upload_to="promociones/", null=True, blank=True,default="images/no_image.png")
    categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE,blank=True,null=True)
    membresia=models.ForeignKey(Membresia,on_delete=models.CASCADE,blank=True,null=True)
    descuento_categoria=models.PositiveIntegerField(blank=True,null=True)
    descuento_membresia=models.PositiveIntegerField(blank=True,null=True)
    activo=models.BooleanField(default=True)