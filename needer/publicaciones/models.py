from django.db import models
from users.models import User
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse

# Create your models here.
def postDirectory(instance, filename):
    profile_picture_name = 'publicacion/{0}/%Y/%m/%d/{1}'.format(instance.username, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    return profile_picture_name


# Funcion para validar que la extension sea correcta
def valid_file_extention(value):
    # TODO VALIDAR FUNCIONAMIENTO
    ext = os.path.splitext(value.name)[1]
    valid_extentions = ['.jpg', '.png', '.gif', '.jpeg', '.mp3', '.mp4', '.wav', '.m4a', '.mov', '.avi', 'mkv', 'webm']
    if not ext.lower() in valid_extentions:
        raise ValidationError('El formato del archivo no es soportado, por favor utiliza cualquiera de los formatos permitidos.')


class Publicacion(models.Model):
    usuario = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='Autor')
    
    # Obligatorio como en reddit.
    titulo = models.CharField(verbose_name='Titulo', max_length=250, blank=False, null=False)

    descripcion = models.CharField(verbose_name='Descripcion', max_length=150, blank=True)
    archivo = models.FileField(upload_to = postDirectory, blank=True, null=True)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha Publicacion', auto_now_add=True, auto_now=False)
    fecha_actualizacion = models.DateTimeField(verbose_name='Fecha Actualizacion', auto_now_add=True)



    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('detalle-publicacion', kwargs={'pk': self.pk})
    


