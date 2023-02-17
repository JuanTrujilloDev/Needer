from django import template
from chat.models import ChatMessage
from django.utils import timezone
from datetime import timedelta
import base64
from django.db.models import Q


register = template.Library()

def get_user(user, thread):

    if thread.first_person == user:
        return thread.second_person

    return thread.first_person

# TODO DESCIFRAR EL MENSAJE
def get_last_message(thread, user):

    if thread.first_person == user:
        if thread.closed_by_first_user:
            return ChatMessage.objects.filter(Q(timestamp__gte=thread.closed_by_first_user)).last()
        else:
            return ChatMessage.objects.filter(thread=thread).order_by('-timestamp').last()
            
    elif thread.second_person == user:
        if thread.closed_by_second_user:
            return ChatMessage.objects.filter(Q(timestamp__gte=thread.closed_by_second_user))
        else:
                return ChatMessage.objects.filter(thread=thread).order_by('-timestamp')
                
    return False

def get_date(date):
    now = timezone.now()
    time = date
    time_left = now - time
    if time_left.seconds/3600 < timezone.timedelta(hours=24).total_seconds()/3600:
         return time.strftime('%I:%M %p')

    elif time_left.seconds/3600 > timezone.timedelta(hours=24).total_seconds()/3600 and time_left.seconds/3600 < timezone.timedelta(hours=48).total_seconds()/3600 :
        return 'Ayer'

    elif time_left.seconds/3600 > timezone.timedelta(hours=48).total_seconds()/3600 and time_left.seconds/3600 < timezone.timedelta(hours=168).total_seconds()/3600:
        return time.strftime('%A')

    else:
        return time.strftime('%d/%B/%Y')

def get_chat_date(date):
    now = timezone.now()
    time = date
    time_left = now - time

    if time_left.seconds/3600 < timezone.timedelta(hours=24).total_seconds()/3600:
         return time.strftime('%I:%M %p')

    elif time_left.seconds/3600 > timezone.timedelta(hours=24).total_seconds()/3600 and time_left.seconds/3600 < timezone.timedelta(hours=48).total_seconds()/3600 :
        return 'Ayer a las ' + time.strftime('%I:%M %p')

    elif time_left.seconds/3600 > timezone.timedelta(hours=48).total_seconds()/3600 and time_left.seconds/3600 < timezone.timedelta(hours=168).total_seconds()/3600:
        return time.strftime('%A') + ' a las ' + time.strftime('%I:%M %p')

    else:
        return time.strftime('%d/%B/%Y') + ' a las ' + time.strftime('%I:%M %p')


    

# TODO Timestamp del chat





register.filter('get_user', get_user)
register.filter('get_last_message', get_last_message)
register.filter('get_date', get_date)
register.filter('get_chat_date', get_chat_date)