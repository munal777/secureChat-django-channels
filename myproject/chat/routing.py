from django.urls import path, re_path
from .consumers import EchoConsumer, PrivateChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', PrivateChatConsumer.as_asgi()),
]