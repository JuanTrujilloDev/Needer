from django import template
from chat.models import ChatMessage
from django.utils import timezone
from datetime import timedelta
import base64


register = template.Library()

def get_user(user, thread):

    if thread.first_person == user:
        return thread.second_person

    return thread.first_person

# TODO DESCIFRAR EL MENSAJE
def get_last_message(thread):
  
    messages = ChatMessage.objects.filter(thread=thread)

    if  messages:
       return messages.latest('timestamp')

    return None

def get_date(date):
    now = timezone.now()
    time = date
    time_left = now - time
    if time.strftime('%A') == now.strftime('%A'):
         return time.strftime('%I:%M %p')

    elif time_left > timedelta(hours=24) and time_left < timedelta(hours=48) :
        return 'Yesterday'

    elif time_left > timedelta(hours=48) and time_left > timedelta(hours=168):
        return time.strftime('%A')

    else:
        return time.strftime('%d/%B/%Y')

def decode_messsage(msg):
    msg = msg.encode('ascii')
    msg = base64.b64decode(msg)
    msg = msg.decode('ascii')

    return msg
    

# TODO Timestamp del chat





register.filter('get_user', get_user)
register.filter('get_last_message', get_last_message)
register.filter('get_date', get_date)
register.filter('decode_message', decode_messsage)