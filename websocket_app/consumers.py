import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class WebsocketConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "abc"
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()


    # Receive message from WebSocket
    def receive(self, text_data):
        self.send(text_data=json.dumps({"server message":f"Hurrah i have receieved the message {text_data}"}))

    def disconnect(self, close_code):
        pass
        # Leave room group
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name, self.channel_name
        # )
