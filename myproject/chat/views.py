from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .utils import make_room_name, decrypt_message
from .models import Message, ChatRoom

User = get_user_model()

@login_required
def chat_view(request, room_name):
    room_members_id = room_name.split('_')

    members_list = []

    for member_id in room_members_id:
        try:
            user = User.objects.get(id=int(member_id))

            if not user.id == request.user.id:
                members_list.append(user.username)            

        except User.DoesNotExist:
            return redirect('dashboard')
    
    members_name = " & ".join(members_list)

    messages = Message.objects.filter(room_name=room_name).order_by("timestamp")

    message_contents = []

    for message in messages:
        try:
            decrypted_msg = decrypt_message(message.content)
        except Exception:
            decrypted_msg = "[Decryption Failed]"

        message_contents.append({
            "sender": message.sender,
            "timestamp": message.timestamp,
            "content": decrypted_msg
        })
        
    return render(request, 'chat.html', {
        'room_name': room_name,
        'room_member': members_name,
        'messages': message_contents,
    })


@login_required
def dashboard_view(request):
    current_user = request.user
    users = User.objects.exclude(id=request.user.id)

    user_rooms = [
        {
            "username": user.username,
            "room_name": make_room_name(current_user.id, user.id),
            # "room_member": f"{current_user.username} {user.username}"
        }
        for user in users
    ]

    return render(request, "dashboard.html", {
        "user_rooms": user_rooms
    })



def landing_page_view(request):
    return render(request, 'landing.html')


@login_required
def create_group_view(request):
    if request.method == "POST":
        group_name = request.POST["room_name"]
        member_ids = request.POST.getlist("members")

        room = ChatRoom.objects.create(name=group_name, is_group=True)
        room.members.set(User.objects.filter(id__in = member_ids))
        room.members.add(request.user)
        room.save()

        return render("chat_room", room_name=room.name)