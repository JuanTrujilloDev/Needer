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
    fecha_actualizacion = models.DateTimeField(verbose_name='Fecha Actualizacion',  auto_now=True)



    def get_absolute_url(self):
        return reverse('detalle-publicacion', kwargs={'pk': self.pk, 'user_slug': self.user.slug})


    def save(self, *args, **kwargs):
        if self.archivo.file.content_type.split('/')[0] == 'image':
            return super().save(*args, **kwargs)
            file_compression(self.archivo)

        else:
            file_compression(self.archivo)
            return super().save(*args, **kwargs)


    def delete(self, using=None, keep_parents=False):
        self.archivo.storage.delete(self.archivo.name)
        super().delete()


        

        
    


