from channels.db import database_sync_to_async
from .models import Message
from django.conf import settings
from cryptography.fernet import Fernet

@database_sync_to_async
def save_message(user, room_name, message):
    encrypted_msg = encrypt_message(message)
    Message.objects.create(sender=user, room_name=room_name, content=encrypted_msg)


def make_room_name(id1, id2):
    return f"{min(id1, id2)}_{max(id1, id2)}"



cipher = Fernet(settings.FERNET_SECRET_KEY)


def encrypt_message(plain_text):
    return cipher.encrypt(plain_text.encode()).decode()


def decrypt_message(cipher_text):
    return cipher.decrypt(cipher_text.encode()).decode()