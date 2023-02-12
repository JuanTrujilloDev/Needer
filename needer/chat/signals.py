from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ChatMessage, Thread


@receiver(post_save, sender= ChatMessage)
def message_create(sender, created, instance, **kwargs):
    if created:
        thread = Thread.objects.get(id = instance.thread.pk)
        thread.timestamp = instance.timestamp
        thread.save()


# TODO AGREGAR QUE CUANDO SE ACTUALIZA LO DE BORRAR SE BORREN LOS MENSAJES
