from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ChatMessage, Thread
from django.utils import timezone
from django.db.models import Q


@receiver(post_save, sender= ChatMessage)
def message_create(sender, created, instance, **kwargs):
    if created:
        thread = Thread.objects.get(id = instance.thread.pk)
        thread.updated = instance.timestamp
        thread.save()

@receiver(pre_save, sender= Thread)
def thread_create(sender,  instance, **kwargs):
    if instance.pk == None:
        instance.closed_by_first_user = timezone.now()
        instance.closed_by_second_user = timezone.now()
        instance.updated = timezone.now()
        
