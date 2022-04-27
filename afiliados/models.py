from django.db import models
from seguridad.models import UserDetails
# Create your models here.

class RegistroNovacoin(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    usuario=models.ForeignKey(UserDetails,on_delete=models.PROTECT)
    novacoins=models.PositiveIntegerField(blank=False,null=False)
    sucursal=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now=True)
