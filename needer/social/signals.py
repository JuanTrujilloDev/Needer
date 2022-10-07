from django.db.models.signals import pre_save, m2m_changed, post_init
from django.dispatch import receiver
from users.models import User
from .models import Publicacion#, LikedPublicacion
from django.utils.text import slugify
from django.core.exceptions import ValidationError

""" Le crea un objeto cuando se crea una publicacion """
""" @receiver(post_init, sender=Publicacion) 
def guardarPerfil(sender, instance, **kwargs):
    Liked_Publicacion.objects.create(id_publicacion = instance) """

