from django.contrib import admin
from .models import Message, ChatRoom

# Register your models here.
admin.site.register(Message)
admin.site.register(ChatRoom)