from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ChatMessage, Thread

# TODO seguridad de mensajes si el usuario pertenece al thread

@receiver(post_save, sender= ChatMessage)
def message_create(sender, created, instance, **kwargs):
    if created:
        thread = Thread.objects.get(id = instance.thread.pk)
        thread.timestamp = instance.timestamp
        thread.save()


# TODO AGREGAR QUE CUANDO SE ACTUALIZA LO DE BORRAR SE BORREN LOS MENSAJES
# TODO Revisar que usuario es el first o second
# TODO si el usuario crea un mensaje nuevo y la fecha de creacion es mayor a closed_by que el closed_by quede nulo
# TODO si el closed_by de ambos es mayor al timestamp se elimina el thread y todos los mensajes