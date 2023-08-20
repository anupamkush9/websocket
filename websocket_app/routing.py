# chat/routing.py
from django.urls import re_path

from websocket_app.consumers import MySyncConsumer, MyAsyncConsumer

websocket_urlpatterns = [
    re_path(r'ws/sync_consumer/(?P<room_name>\w+)/$', MySyncConsumer.as_asgi()),
    re_path(r"ws/async_consumer/(?P<room_name>\w+)/$", MyAsyncConsumer.as_asgi()),
]