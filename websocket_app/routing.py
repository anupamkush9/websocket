# chat/routing.py
from django.urls import re_path

from websocket_app.consumers import MySyncConsumer, MyAsyncConsumer

websocket_urlpatterns = [
    re_path(r"ws/sync_consumer/$", MySyncConsumer.as_asgi()),
    re_path(r"ws/async_consumer/$", MyAsyncConsumer.as_asgi()),
]