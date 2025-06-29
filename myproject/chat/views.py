from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .utils import make_room_name

User = get_user_model()

@login_required
def chat_view(request, room_name):
    return render(request, 'chat.html', {'room_name': room_name})



def chat_user_list(request):
    users = User.objects.exclude(id=request.user.id)

    return render(request, "dashboard.html", {
        "users": users,
        "make_room_name": make_room_name,
    })