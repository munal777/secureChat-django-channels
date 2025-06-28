from django.urls import path
from .consumers import EchoConsumer, PublicChatConsumer
import re

websocket_urlpatterns = [
    path('ws/echo/', EchoConsumer.as_asgi()),
    path(r'ws/chat/(?P<room_name>\w+)/$', PublicChatConsumer.as_asgi()),
]