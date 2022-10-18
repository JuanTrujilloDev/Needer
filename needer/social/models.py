
from operator import mod
from colorama import Fore

from django.db import models
from users.models import User
from django.urls import reverse
from tinymce.models import HTMLField
from .utils import *
import os
from needer import settings




class Publicacion(models.Model):

    class Meta:
        verbose_name_plural = "Publicaciones"

        
    user = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='Autor')
    

    descripcion = HTMLField(verbose_name='Descripcion', max_length=2200, null=True, blank=True)
    archivo = models.FileField(upload_to = postDirectory, blank=True, null=True, validators=[valid_file_extention, valid_file_size])
    fecha_creacion = models.DateTimeField(verbose_name='Fecha Publicacion', auto_now_add=True, auto_now=False)
    fecha_actualizacion = models.DateTimeField(verbose_name='Fecha Actualizacion',  auto_now=True, auto_now_add=False, blank=True, null=True)
    nsfw = models.BooleanField(verbose_name='NSFW', default=False, null=False, blank=False)



    def get_absolute_url(self):
        return reverse('detalle-publicacion', kwargs={'pk': self.pk, 'user_slug': self.user.slug})


    def save(self, *args, **kwargs):
        
        # Si se esta creando el objeto
        if self._state.adding:
            if self.archivo:
                if self.archivo.file.content_type.split('/')[0] == 'image':
                    # file_compression(self.archivo)
                    return super().save(*args, **kwargs)
                    

                else:
                    file_compression(self.archivo)
                    return super().save(*args, **kwargs)

        return super().save(*args, **kwargs)


    def delete(self, using=None, keep_parents=False):
        if self.archivo:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, self.archivo.name))
            except:
                pass
        super().delete()


    def likePublicacion(self): return reverse('addlike', kwargs={'pk':self.id})
    def disPublicacion(self): return reverse('removelike', kwargs={'pk':self.id})



class LikedPublicacion(models.Model):
    id_publicacion = models.ForeignKey(Publicacion, verbose_name= ("Publicacion"), on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, verbose_name= ("Usuario"), on_delete=models.CASCADE)
    fecha = models.DateTimeField(verbose_name = 'Fecha de Like' ,auto_now_add=True, auto_now=False)


class Comentarios(models.Model):
    id_publicacion = models.ForeignKey(Publicacion, verbose_name= ("Publicacion"), on_delete=models.CASCADE)
    id_autor = models.ForeignKey(User, verbose_name= ("Autor"), on_delete=models.CASCADE)
    comentario = models.TextField(max_length=520, verbose_name=("Comentario"), blank=False)
    fecha_creacion = models.DateTimeField(verbose_name = 'Fecha de Like', auto_now_add=True, auto_now=False)
    
    def likeComentario(self): return reverse('comentario-addlike', kwargs={'pk':self.id})
    def dislikeComentario(self): return reverse('comentario-removelike', kwargs={'pk':self.id})
    def urlComentario(self): return reverse('delete-comentario', kwargs={'pk':self.id,'user_slug':self.id_autor.slug})
    

class LikeComentarios(models.Model):
    id_comentario = models.ForeignKey(Comentarios, verbose_name= ("Comentarios"), on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, verbose_name= ("Usuario"), on_delete=models.CASCADE)
    fecha = models.DateTimeField(verbose_name = 'Fecha de Like' ,auto_now_add=True, auto_now=False)

        

        
    


