import json
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
import time
from websocket_app.models import Chat, Group
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket  # Import your Ticket model
from channels.layers import get_channel_layer

class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("ticket_updates", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("ticket_updates", self.channel_name)

    async def send_update(self, event):
        print("evenet:::",event)
        await self.send(text_data=json.dumps(event["message"]))

@receiver(post_save, sender=Ticket)
def send_ticket_update(sender, instance, created, **kwargs):
    print("post save signal claeed", f"just now instance :: {instance.title} is updated")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "ticket_updates",  # Group name
        {
            "type": "send.update",
            "message": f"just now instance :: {instance.title} is updated",
        },
    )

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
        if self.scope['user'].is_authenticated :
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
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_name, {"type": "chat.message", "message": {"user": "Annonymous user", "message": "Login Required"}}
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

        print("--user-----_>", self.scope['user'])
        print("--username-----_>", self.scope['user'].username)
        print("--dir(user)-----_>", dir(self.scope['user']))
        print("---.self.scope['user'].is_authenticated----", self.scope['user'].is_authenticated)
        if self.scope['user'].is_authenticated :
            group  = await database_sync_to_async(Group.objects.get)(name = self.room_name)
            print("------->",group)
            print("---type---->",type(group))
            chat = Chat(content=text_data_json["message"],
                        group=group)
            await database_sync_to_async(chat.save)()
            text_data_json["user"] = self.scope['user'].username
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_name, {"type": "chat.message", "message": text_data_json}
            )
        else:
            await self.channel_layer.group_send(
                self.room_name, {"type": "chat.message", "message": {"user": "Annonymous user", "message": "Login Required"}}
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
                "text": json.dumps(text_data_json),
            })

    async def websocket_disconnect(self, event):
        print("sync websocket consumer disconnect")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name, self.channel_name
        )
        raise StopConsumer()


class MyWebsocketConsumer(WebsocketConsumer):

    def connect(self):
        # To accept the connection call:
        # Called on connection.
        print("connection established", self)
        self.accept()
        # # Or accept the connection and specify a chosen subprotocol.
        # # A list of subprotocols specified by the connecting client
        # # will be available in self.scope['subprotocols']
        # self.accept("subprotocol")
        # To reject the connection, call:
        # self.close()

    def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        print("text_data:::", text_data)
        for i in range(20):
            time.sleep(1)
            self.send(text_data=json.dumps({"message":str(i)}))
        # Or, to send a binary frame:
        # self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        # self.close()
        # Or add a custom WebSocket error code!
        # self.close(code=4123)

    # def disconnect(self, close_code):
    #     print("Disconnecting.........")
        # Called when the socket closes

