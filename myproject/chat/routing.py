from django.urls import re_path
from .consumers import PrivateChatConsumer, GroupChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/private/(?P<room_name>\w+)/$', PrivateChatConsumer.as_asgi()),
    re_path(r'ws/chat/group/(?P<room_name>\w+)/$', PrivateChatConsumer.as_asgi()),
]