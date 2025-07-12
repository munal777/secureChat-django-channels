from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .utils import save_message
from .models import ChatRoom
import json

class PrivateChatConsumer(AsyncWebsocketConsumer):
    """
    Handles real-time private messaging between two users over WebSocket.
    """

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        users_id = self.room_name.split('_')
        if str(self.scope["user"].id) not in users_id:
            await self.close()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def receive(self, text_data):
        data= json.loads(text_data)
        user = self.scope["user"]


        if data.get("type") == "file":
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_file',
                'filename': data['filename'],
                'mimetype': data['mimetype'],
                'data': data['data'],
                'sender': user.username,
            }
            )
            
        if data.get("type") == "voice":
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'voice_message',
                'filename': data['filename'],
                'mimetype': data['mimetype'],
                'data': data['data'],
                'sender': user.username,
            }
            )
            
                
        if data.get('type') == "text": 
            message = data['message']

            # Save the message in the DB
            await save_message(user, self.room_name, message)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': user.username
                }
            )
        
    async def chat_file(self, event):
        await self.send(text_data=json.dumps({
            'type': 'file',
            'sender': event['sender'],
            'filename': event['filename'],
            'mimetype': event['mimetype'],
            'data': event['data'],
        }))

    async def voice_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'voice',
            'sender': event['sender'],
            'filename': event['filename'],
            'mimetype': event['mimetype'],
            'data': event['data'],
        }))

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'message': event['message'],
                    'sender': event['sender']
                }
            )
        )
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


class GroupChatConsumer(AsyncWebsocketConsumer):
    """
    Handles real-time group messaging between many users over WebSocket.
    """

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        try:
            room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)
            is_member = await database_sync_to_async(room.members.filter(id=self.user.id).exists)()

            if not is_member:
                await self.close()
                return
        except ChatRoom.DoesNotExist:
            await self.close()
            return
        

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    

    async def receive(self, text_data):
        data= json.loads(text_data)
        user = self.scope["user"]


        if data.get("type") == "file":
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_file',
                'filename': data['filename'],
                'mimetype': data['mimetype'],
                'data': data['data'],
                'sender': user.username,
            }
            )
            
        if data.get("type") == "voice":
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'voice_message',
                'filename': data['filename'],
                'mimetype': data['mimetype'],
                'data': data['data'],
                'sender': user.username,
            }
            )
            
                
        if data.get('type') == "text": 
            message = data['message']

            # Save the message in the DB
            await save_message(user, self.room_name, message)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': user.username
                }
            )
    
    async def chat_file(self, event):
        await self.send(text_data=json.dumps({
            'type': 'file',
            'sender': event['sender'],
            'filename': event['filename'],
            'mimetype': event['mimetype'],
            'data': event['data'],
        }))

    async def voice_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'voice',
            'sender': event['sender'],
            'filename': event['filename'],
            'mimetype': event['mimetype'],
            'data': event['data'],
        }))

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'message': event['message'],
                    'sender': event['sender']
                }
            )
        )
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
