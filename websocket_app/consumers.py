import json
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
import time

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })
        print("sync websocket connection established")

    def websocket_receive(self, event):
        message = event['text']
        print("websocket received", message)
        for i in range(50):
            self.send({
                "type": "websocket.send",
                "text": str(i),
            })
            time.sleep(1)
    
    def websocket_disconnect(self, event):
        print("sync websocket consumer disconnect")
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })
        print("Async websocket connection established")

    async def websocket_receive(self, event):
        for i in range(50):
            await self.send({
                "type": "websocket.send",
                "text": str(i),
            })
            time.sleep(1)


    def websocket_disconnect(self, event):
        print("Async websocket consumer disconnect")
        raise StopConsumer()
