# chat/routing.py
from django.urls import re_path

from websocket_app.consumers import WebsocketConsumer

websocket_urlpatterns = [
    re_path(r"ws/websocket_home/$", WebsocketConsumer.as_asgi()),
]