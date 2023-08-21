import json
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
import time
from websocket_app.models import Chat, Group
from channels.db import database_sync_to_async

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )
        self.send({
            "type": "websocket.accept",
        })
        print("sync websocket connection established")

    def websocket_receive(self, event):
        print("event:::", event)
        print("eve type nt:::", type(event))
        print("dir(event):::", dir(event))
        text_data_json = json.loads(event.get("text"))
        print("text_data_json:::", text_data_json)
        print("text_data_json:::", type(text_data_json))
        message = text_data_json["message"]
        
        group = Group.objects.get(name = self.room_name)
        print("------->",group)
        print("---type---->",type(group))
        chat = Chat(content=text_data_json["message"],
                    group=group)
        chat.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {"type": "chat.message", "message": text_data_json}
        )

    # Receive message from room group
    def chat_message(self, event):
        print("chat_message event:::", event)
        print("chat_message eve type nt:::", type(event))
        print("chat_message dir(event):::", dir(event))
        text_data_json = event.get("message")
        print("text_data_json:::", text_data_json)
        print("text_data_json:::", type(text_data_json))
        message = text_data_json["message"]
        print("emssage:::", message)
        print("typeof message", type(message))

        # Send message to WebSocket
        # self.send(json.dumps({"message": message}))
        self.send({
                "type": "websocket.send",
                "text": message,
            })

    def websocket_disconnect(self, event):
        print("sync websocket consumer disconnect")
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # Join room group
        await self.channel_layer.group_add(
            self.room_name, self.channel_name
        )
        await self.send({
            "type": "websocket.accept",
        })
        print("Async websocket connection established")

    async def websocket_receive(self, event):
        print("event:::", event)
        print("eve type nt:::", type(event))
        print("dir(event):::", dir(event))
        text_data_json = json.loads(event.get("text"))
        print("text_data_json:::", text_data_json)
        print("text_data_json:::", type(text_data_json))
        message = text_data_json["message"]

        group  = await database_sync_to_async(Group.objects.get)(name = self.room_name)
        print("------->",group)
        print("---type---->",type(group))
        chat = Chat(content=text_data_json["message"],
                    group=group)
        await database_sync_to_async(chat.save)()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name, {"type": "chat.message", "message": text_data_json}
        )


    # Receive message from room group
    async def chat_message(self, event):
        print("chat_message event:::", event)
        print("chat_message eve type nt:::", type(event))
        print("chat_message dir(event):::", dir(event))
        text_data_json = event.get("message")
        print("text_data_json:::", text_data_json)
        print("text_data_json:::", type(text_data_json))
        message = text_data_json["message"]
        print("emssage:::", message)
        print("typeof message", type(message))

        # Send message to WebSocket
        await self.send({
                "type": "websocket.send",
                "text": message,
            })

    async def websocket_disconnect(self, event):
        print("sync websocket consumer disconnect")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name, self.channel_name
        )
        raise StopConsumer()
