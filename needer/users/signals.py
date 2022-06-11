from allauth.account.signals import user_signed_up
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from .models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError






@receiver(user_signed_up)
def user_signed(request, user, **kwargs):
    """
    user_signed

    When user sign ups it slugify the username
    ONLY if the user is Creador de contenido.

    Else it sets photo and slug to None
    
    """
    user.slug = slugify(user.username)
    user.apodo = user.slug


    user.save()


@receiver(pre_save, sender = User)
def user_update(sender, instance, **kwargs):
    """
    user_update

    When user update his information it slugify the username

    
    """

    instance.slug = slugify(instance.username)






    
            


