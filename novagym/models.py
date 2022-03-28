from django.db import models
from seguridad.models import UserDetails


class ProgresoImc(models.Model):
    class Meta:
        ordering = ["-created_at"]

    usuario = models.ForeignKey(
        UserDetails, on_delete=models.CASCADE, related_name="progreso_imc")
    peso = models.DecimalField(max_digits=5, decimal_places=2)  # kilogramos
    estatura = models.DecimalField(max_digits=5, decimal_places=2)  # metros
    resultado = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def calcular_imc(self):
        resultado = self.peso/self.estatura**2
        return resultado
      
    def save(self, *args, **kwargs):
        self.resultado = self.calcular_imc()
        return super().save(*args, **kwargs)