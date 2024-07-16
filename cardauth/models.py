from django.db import models

from seguridad.models import UserDetails
from django.contrib.auth.models import User



# Create your models here.
class Cardauth(models.Model):
    id_cardauth = models.AutoField(primary_key=True)
    usuario     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=100)
    subtoken =  models.CharField(max_length=20)
    lastDigits = models.CharField(max_length=4, default='0000')
    payerDocument = models.CharField(max_length=20, default= '0000000')
    payerDocumentType = models.CharField(max_length=20, default= '0000000')
    payerName = models.CharField(max_length=20, default= '0000000')
    payerSurname = models.CharField(max_length=20, default= '0000000')
    payerEmail = models.CharField(max_length=20, default= '0000000')
    payerMobile = models.CharField(max_length=20, default= '0000000')
    
    
    def __str__(self):
        return str(self.id_cardauth)+"-"+str(self.token)+"-"+str(self.subtoken)+"-"+str(self.subtoken)+"-"+str(self.lastDigits)
