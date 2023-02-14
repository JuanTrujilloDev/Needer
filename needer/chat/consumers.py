import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db.models import Q
import base64
from datetime import datetime


from chat.models import Thread, ChatMessage

User = get_user_model()


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        """ print('connected', event) """
        user = self.scope['user']
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
        """ print('receive', event) """
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')
        request_user = received_data.get('request_user')
        

        if not msg:
            
            return False
        request_user = await self.user_in_thread(request_user, thread_id)
        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)
        
        if request_user:
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
        else:
            return False
        
        
    


    async def websocket_disconnect(self, event):
        pass

    async def chat_message(self, event):
        
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def user_in_thread(self, user_id, thread_id):
        request_user = User.objects.get(id = user_id)
        thread = Thread.objects.filter((Q(id = thread_id) & (Q(first_person = request_user) | Q(second_person = request_user)) ))
        if thread.exists():
            obj = thread.first()
        else:
            obj = None
        return obj


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
            msg = msg.encode('ascii')
            msg = base64.b64encode(msg)
            msg = msg.decode('ascii')
            print(msg)
            ChatMessage.objects.create(thread=thread, user=user, message=msg)
        return False

    