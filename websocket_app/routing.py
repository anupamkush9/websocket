# chat/routing.py
from django.urls import re_path

from websocket_app.consumers import MyJsonWebsocketConsumer, MyAsyncJsonWebsocketConsumer

websocket_urlpatterns = [
    # re_path(r'ws/sync_consumer/(?P<room_name>\w+)/$', MySyncConsumer.as_asgi()),
    # re_path(r"ws/async_consumer/(?P<room_name>\w+)/$", MyAsyncConsumer.as_asgi()),
    # re_path(r"ws/websocket_consumer/$", MyWebsocketConsumer.as_asgi()),
    # re_path(r"ws/asyncwebsocket_consumer/$", MyAsyncWebsocketConsumer.as_asgi()),
    re_path(r"ws/My_JsonWebsocketConsumer/$", MyJsonWebsocketConsumer.as_asgi()),
    re_path(r"ws/My_AsyncJsonWebsocketConsumer/$", MyAsyncJsonWebsocketConsumer.as_asgi()),
    
]