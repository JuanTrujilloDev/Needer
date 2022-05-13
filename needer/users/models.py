from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.

class Pais(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
    
    class Meta:
        ordering = ["nombre"]
        verbose_name = "Pais"
        verbose_name_plural = "Paises"
        
    def __str__(self) -> str:
        return self.nombre
        

class User(AbstractUser):
    
    groups = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name="Groups")
    
    # Datos personales de facturacion.
        
    num_documento = models.CharField(verbose_name='Numero de documento', max_length=10, null = True, blank = True, unique=True)
    pais = models.ForeignKey(Pais, verbose_name="Pais", null=True, blank=True, on_delete=models.SET_NULL)
    # TODO NUMERO DE CELULAR
    direccion_facturacion = models.CharField(verbose_name='Direccion', max_length=120, null = True, blank= True)
    
        
        
        
        

    
    
