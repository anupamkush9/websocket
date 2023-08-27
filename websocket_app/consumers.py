import json
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
import time
from .models import Chat, Group
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer


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


class MyWebsocketConsumer(WebsocketConsumer):
    # groups = ["broadcast"]

    def connect(self):
        # Called on connection.
        # To accept the connection call:
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )
        self.accept()
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        # self.accept("subprotocol")
        # To reject the connection, call:
        # self.close()

    def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        client_data = json.loads(text_data)

        group = Group.objects.get(name = self.room_name)
        print("------->",group)
        print("---type---->",type(group))
        chat = Chat(content=client_data["message"],
                    group=group)
        chat.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {"type": "chat.message", "message": client_data}
        )

        # Or, to send a binary frame:
        # self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        # self.close()
        # Or add a custom WebSocket error code!
        # self.close(code=4123)

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))


    def disconnect(self, close_code):
        print("Websocket disconnected...")
        # Called when the socket closes

class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
    # groups = ["broadcast"]

    def connect(self):
        # Called on connection.
        # To accept the connection call:
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )
        self.accept()
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        # self.accept("subprotocol")
        # To reject the connection, call:
        # self.close()

    def receive_json(self,content = None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        # client_data = json.loads(text_data)
        print("-->", content)
        print("-->", type(content))

        group = Group.objects.get(name = self.room_name)
        print("------->",group)
        print("---type---->",type(group))
        chat = Chat(content=content.get("message"),
                    group=group)
        chat.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {"type": "chat.message", "message": content}
        )

        # Or, to send a binary frame:
        # self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        # self.close()
        # Or add a custom WebSocket error code!
        # self.close(code=4123)

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send_json(message)


    def disconnect(self, close_code):
        print("Websocket disconnected...")
        # Called when the socket closes
