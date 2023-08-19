import json
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })
        print("sync websocket connection established")

    def websocket_receive(self, event):
        self.send({
            "type": "websocket.send",
            "text": event["text"],
        })
        print("sync websocket connection received")


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })
        print("Async websocket connection established")

    async def websocket_receive(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })
        print("Async consumer websocket connection received")
