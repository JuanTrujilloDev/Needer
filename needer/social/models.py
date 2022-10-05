from colorama import Fore
from django.db import models
from users.models import User
from django.urls import reverse
from tinymce.models import HTMLField
from .utils import *




class Publicacion(models.Model):

    class Meta:
        verbose_name_plural = "Publicaciones"

        
    user = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='Autor')
    

    descripcion = HTMLField(verbose_name='Descripcion', max_length=280, null=True, blank=True)
    archivo = models.FileField(upload_to = postDirectory, blank=True, null=True, validators=[valid_file_extention, valid_file_size])
    fecha_creacion = models.DateTimeField(verbose_name='Fecha Publicacion', auto_now_add=True, auto_now=False)
    fecha_actualizacion = models.DateTimeField(verbose_name='Fecha Actualizacion',  auto_now=True, auto_now_add=False, blank=True, null=True)
    nsfw = models.BooleanField(verbose_name='NSFW', default=False, null=False, blank=False)



    def get_absolute_url(self):
        return reverse('detalle-publicacion', kwargs={'pk': self.pk, 'user_slug': self.user.slug})


    def save(self, *args, **kwargs):
        if self.archivo:
            if self.archivo.file.content_type.split('/')[0] == 'image':
                return super().save(*args, **kwargs)
                file_compression(self.archivo)

            else:
                file_compression(self.archivo)
                return super().save(*args, **kwargs)

        return super().save(*args, **kwargs)


    def delete(self, using=None, keep_parents=False):
        self.archivo.storage.delete(self.archivo.name)
        super().delete()


class LikedPublicacion(models.Model):
    id_publicacion = models.ForeignKey(Publicacion, verbose_name= ("Likes"), on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, verbose_name= ("Likes de Usuarios"), on_delete=models.CASCADE)
    fecha = models.DateTimeField(verbose_name = 'Fecha de Like' ,auto_now_add=True, auto_now=False)

    



        

        
    


