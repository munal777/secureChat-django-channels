from channels.consumer import SyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class EchoConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        text = event.get("text","")

        if text.lower() == "hi":
            response = "Hello! how may I help you!"
        elif text.lower() == "bye":
            response = "Goodbye!"
        else:
            response = f"Client message: {text}"

        self.send({
            "type": "websocket.send",
            "text": response,
        })

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "chatroom"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', # handler name to be called
                'message': message
            }
        )

    # custom event handler that is called automatically when msg is send to group using group_send()
    async def chat_message(self, event):
        message = event['message']

        # send method sends data to client
        await self.send(text_data=json.dumps({
            'message': message
        })) 
    
    async def disconnect(self, code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

