from django.db import models

from seguridad.models import UserDetails

# Create your models here.
class Cardauth(models.Model):
    id_cardauth = models.AutoField(primary_key=True)
    token = models.CharField(max_length=20)
    auth = models.CharField(max_length=3)
    
    def __str__(self):
        return str(self.id_cardauth)+"-"+str(self.token)+"-"+str(self.cvc)
