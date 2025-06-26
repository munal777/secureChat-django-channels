from django.urls import path
from .consumers import EchoConsumer, ChatConsumer

websocket_urlpatterns = [
    path('ws/echo/', EchoConsumer.as_asgi()),
    path('ws/chat', ChatConsumer.as_asgi()),

]