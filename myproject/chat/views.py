from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .utils import make_room_name

User = get_user_model()

@login_required
def chat_view(request, room_name):
    return render(request, 'chat.html', {'room_name': room_name})


@login_required
def dashboard_view(request):
    current_user = request.user
    users = User.objects.exclude(id=request.user.id)

    user_rooms = [
        {
            "username": user.username,
            "room_name": make_room_name(current_user.id, user.id),
        }
        for user in users
    ]

    return render(request, "dashboard.html", {
        "user_rooms": user_rooms
    })