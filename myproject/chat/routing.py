from django.urls import path
from .consumers import EchoConsumer, PublicChatConsumer

websocket_urlpatterns = [
    path('ws/echo/', EchoConsumer.as_asgi()),
    path('ws/chat/', PublicChatConsumer.as_asgi()),
]