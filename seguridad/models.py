from django.contrib.auth.models import User
from django.db import models

from seguridad import validators

# Create your models here.


class UserDetails(models.Model):
    class Meta:
        ordering = ['-created_at']

    class Sex(models.TextChoices):
        MAN = 'H', 'Hombre'
        WOMEN = 'M', 'Mujer'
        NON = 'N', 'No especificar'

    class Tipo(models.TextChoices):
        CLI = 'C', 'Cliente'
        EMP = 'E', 'Empleado'

    class Device(models.TextChoices):
        PC = 'PC', 'Administrador PC'
        MOB = 'MOB', 'App Movíl'

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="detalles")
    codigo = models.CharField(max_length=255, blank=True)
    cedula = models.CharField(max_length=13, validators=[
                              validators.validate_ci])
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='usuario/', null=True, blank=True)
    telefono = models.CharField(max_length=12, validators=[
                                validators.validate_phone])
    sexo = models.CharField(max_length=2, choices=Sex.choices)
    tipo = models.CharField(max_length=2, choices=Tipo.choices, default='E')
    fecha_nacimiento = models.DateField()
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    created_from = models.CharField(
        max_length=24, choices=Device.choices, default=Device.PC)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.usuario.email +' - '+ self.cedula + ' - ' + self.apellidos + ' - ' + self.tipo
    
    @property
    def membresia(self):
        return self.historial_membresia.get(activa=True)
      
    @property
    def tiene_membresia(self):
        return self.historial_membresia.filter(activa=True).count() > 0
