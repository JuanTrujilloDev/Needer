from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django_resized import ResizedImageField
from django.urls import reverse
from .utils import *

# Create your models here.

class Pais(models.Model):
    """
    Pais

    id -> int
    nombre -> string

    
    """

    nombre = models.CharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
    
    class Meta:
        ordering = ["nombre"]
        verbose_name = "Pais"
        verbose_name_plural = "Paises"
        
    def __str__(self) -> str:
        return self.nombre
        

class TipoCelebridad(models.Model):
    """
    TipoCelebridad

    id -> int
    nombre -> string


    """

    nombre = models.CharField(max_length=24, verbose_name="Nombre", null=False, blank=False)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Tipo Celebridad"
        verbose_name_plural = "Tipos de Celebridad"

    def __str__(self):
        return self.nombre




class User(AbstractUser):
    """
    User Model

    attrs from AbstractUser:
    
    id -> int
    username -> string
    first_name -> string
    last_name -> string
    password -> string(encrypted)
    email -> string
    groups -> comes from Group Model
    num_documento -> string
    pais -> comes from Pais Model
    slug -> string
    biografia -> string
    genero -> string
    fecha_nacimiento -> date
    tipo_celebridad -> comes from TipoCelebridad
    foto -> file
    cartera int
    link link
    methods:

    save(self, *args, **kwargs) -> saves instance

    
    """
    
    
    groups = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name="Groups")
    
    # Datos personales de facturacion.
        
    num_documento = models.CharField(verbose_name='Numero de documento', max_length=10, null = True, blank = True, unique=True)
    pais = models.ForeignKey(Pais, verbose_name="Pais", null=True, blank=True, on_delete=models.SET_NULL)
    # TODO NUMERO DE CELULAR
    direccion_facturacion = models.CharField(verbose_name='Direccion', max_length=120, null = True, blank= True)
    slug = models.SlugField(verbose_name="Slug", null = True, blank=True, unique=True)
    biografia = models.TextField(max_length=200, verbose_name="Bio", blank=True)

    # TODO Telefono


    class GeneroChoices(models.TextChoices):
        HOMBRE = 'Hombre', 'Hombre',
        MUJER = 'Mujer', 'Mujer',
        OTRO = 'Otro', "Otro"

    apodo = models.CharField(max_length=25, blank=True, null=True)
    genero = models.CharField(max_length=7, choices = GeneroChoices.choices, default=GeneroChoices.OTRO)
    fecha_nacimiento = models.DateField(verbose_name="Fecha nacimiento", blank=True, null=True)
    tipo_celebridad = models.ManyToManyField(TipoCelebridad, blank = True)
    foto = ResizedImageField(size=[500,500], upload_to = user_directory_path_profile,  blank=True)
    link = models.CharField(max_length=80, null=True, blank=True)

    # TODO REVISAR DE DOCUMENTACION
    cartera = models.DecimalField(max_digits=19,decimal_places=2, default=0, null=True, blank=True)



    def get_absolute_url(self):
        return reverse('detalle-creador', kwargs={'slug': self.slug})


    
        
    
        
        
        
        

    
    
