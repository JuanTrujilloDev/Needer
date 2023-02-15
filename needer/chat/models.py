from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone

User = get_user_model()

# Create your models here.

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=False)
    closed_by_first_user = models.DateTimeField(auto_now=False, auto_now_add=False)
    closed_by_second_user = models.DateTimeField(auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']

    def get_absolute_url(self):
        return reverse('thread', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.pk:
            thread = Thread.objects.filter((Q(first_person=self.first_person) & Q(second_person=self.second_person)) | (Q(first_person=self.second_person) & Q(second_person=self.first_person)))
            if thread:
                raise ValidationError('Ya existe un chat entre estos dos usuarios')
        return super(Thread, self).save(*args, **kwargs)


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=650)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["timestamp"]

    def save(self,*args, **kwargs):
        if not self.message:
            raise ValidationError('Mensaje vacio')
        elif self.message.strip() == '':
            raise ValidationError('Mensaje vacio')
        else:
            if self.user == self.thread.first_person or self.user == self.thread.second_person:
                return super(ChatMessage, self).save(*args, **kwargs)
            else:
                raise ValidationError('El usuario no pertenece al thread')
        
