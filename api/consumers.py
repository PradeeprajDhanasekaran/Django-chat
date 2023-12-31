from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User, Message
import json

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        my_username = self.scope['user'].username
        my_id = self.scope['user'].id
        self.room_name = my_username
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.change_status(my_id,True)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        other_user_id = data['receiver']
        receiver =  'chat_%s' % other_user_id
        receiver_id = data['receiver']
        username = self.scope['user'].username
        # groupName = '-'.join(sorted([my_username,receiver_id]))
        # # channel_name = f"chat_{groupName}" 
        recipient = await self.get_user_by_id(receiver_id)
        # recipient_exists = await database_sync_to_async(recipient.exists)()
        if  recipient != 'notExist' :
            if recipient :
                await self.save_message( self.room_group_name, message, receiver_id)
                await self.channel_layer.group_send(
                    receiver,
                    {
                        "type": "chat_message",
                        "message": message,
                        "username": username,
                    }
                )
            else:
                await self.send(text_data=json.dumps({
                    'error': 'Recipient is offline',
                }))
        else:
            await self.send(text_data=json.dumps({
                'error': 'Recipient not found',
            }))
    @database_sync_to_async
    def get_user_by_id(self, user_id):
        user = User.objects.filter(username=user_id)
        if user.exists():
            return User.objects.filter(username=user_id).first().online
        return 'notExist'
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        my_id = self.scope['user'].id
        await self.change_status(my_id,False)


    @database_sync_to_async
    def save_message(self, thread_name, message, receiver):
        sender_id = self.scope['user']
        receiver_id = User.objects.get(username=receiver)
        chat_obj = Message.objects.create(
            sender=sender_id, content=message, thread_name=thread_name,recipient=receiver_id)
        
    @database_sync_to_async
    def change_status(self, id, status):
        user = User.objects.get(id=id)
        user.online=status
        user.save()
