from os import access
from django.db import models

# Create your models here.

class Access_Token_Paypal(models.Model):
    access_token = models.CharField(verbose_name='Token de Acceso Paypal', max_length=120, null = True, blank= True)


