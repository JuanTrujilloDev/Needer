from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.

class User(AbstractUser):
    class TipoDocumento(models.TextChoices):
        CEDULA = 'CC', 'Cedula de ciudadania'
        CEDULA_EX = 'CE', 'Cedula de extranjeria'
        PASAPORTE = 'PA', 'Pasaporte'
        
    tipo_documento = models.CharField(verbose_name='Tipo Documento', choices=TipoDocumento.choices, default=TipoDocumento.CEDULA, null=True, blank=True, max_length=40)
    num_documento = models.CharField(verbose_name='Numero de documento', max_length=10, null = True, blank = True, unique=True)
    # TODO ciudad
    # TODO departamento
    # TODO NUMERO DE CELULAR
    direccion_facturacion = models.CharField(verbose_name='Direccion', max_length=120, null = True, blank= True)
    groups = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name="Groups")
        
        
        
        

    
    
