from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User, Message
import json

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        my_id = self.scope['user'].id
        # other_user_id = self.scope['url_route']['kwargs']['id']
        # if int(my_id) > int(other_user_id):
        #     self.room_name = f'{my_id}-{other_user_id}'
        # else:
        #     self.room_name = f'{other_user_id}-{my_id}'
        self.room_name = my_id
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        # receiver = data['receiver']
        other_user_id = self.scope['url_route']['kwargs']['id']
        receiver =  'chat_%s' % other_user_id

        # await self.save_message(username, self.room_group_name, message, receiver)
        await self.channel_layer.group_send(
            receiver ,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )

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

    # @database_sync_to_async
    # def save_message(self, username, thread_name, message, receiver):
    #     chat_obj = ChatModel.objects.create(
    #         sender=username, message=message, thread_name=thread_name)
    #     other_user_id = self.scope['url_route']['kwargs']['id']
    #     get_user = User.objects.get(id=other_user_id)
    #     if receiver == get_user.username:
    #         ChatNotification.objects.create(chat=chat_obj, user=get_user)