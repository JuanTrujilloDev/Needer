from allauth.account.signals import user_signed_up
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User
from django.utils.text import slugify

@receiver(user_signed_up)
def user_signed(request, user, **kwargs):
    """
    user_signed

    When user sign ups it slugify the username
    ONLY if the user is Creador de contenido.

    Else it sets photo and slug to None
    
    """
    if user.groups.name == "Creador de Contenido":
        user.slug = slugify(user.username)

    else:
        user.foto = None
        user.slug = None

    user.save()


@receiver(pre_save, sender = User)
def user_update(sender, instance, **kwargs):
    """
    user_update

    When user update his information it slugify the username
    ONLY if the user is Creador de contenido and it has already
    signup.

    Else it sets photo and slug to None

    
    """
    if instance.groups != None:
        if instance.groups.name == "Creador de Contenido":

            instance.slug = slugify(instance.username)

        else:
            instance.foto = None
            instance.slug = None




    
            


