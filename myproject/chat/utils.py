from channels.db import database_sync_to_async
from .models import Message

@database_sync_to_async
def save_message(user, room_name, message):
    Message.objects.create(sender=user, room_name=room_name, content=message)


def make_room_name(id1, id2):
    return f"{min(id1, id2)}_{max(id1, id2)}"
