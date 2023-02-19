import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "needer.settings")

import django
django.setup()


import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import datetime

from chat.models import Thread, ChatMessage

User = get_user_model()



class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        user = self.scope['user']
        thread_id = self.scope['url_route']['kwargs']['pk']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room

      
        await self.channel_layer.group_add(
                chat_room,
                self.channel_name
            )
        await self.send({
                'type': 'websocket.accept'
            })


    async def websocket_receive(self, event):

        received_data = json.loads(event['text'])
        
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')

        request_user = received_data.get('request_user')
        
        
        
        if not msg:
            
            return False


        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)


        
        if not sent_by_user:
            return False
        if not send_to_user:
            return False
        if not thread_obj:
            return False

        await self.create_chat_message(thread_obj, sent_by_user, msg)

        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user = self.scope['user']
        response = {
                'message': msg,
                'sent_by': self_user.id,
                'thread_id': thread_id,
                'time': datetime.now().strftime('%I:%M %p')
            }

        await self.channel_layer.group_send(
                other_user_chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
                }
            )

        await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
        }
        )
        
        
    


    async def websocket_disconnect(self, event):
        pass

    async def chat_message(self, event):

        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })


    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)

        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        # TODO Seguridad de mensajes
        if thread.first_person == user or thread.second_person == user:
            ChatMessage.objects.create(thread=thread, user=user, message=msg)
        return False

    
