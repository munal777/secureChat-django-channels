from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .utils import make_room_name, decrypted_history_msg
from .models import Message, ChatRoom

User = get_user_model()

@login_required
def chat_view(request, room_name):
    user = request.user

    try:
        room = ChatRoom.objects.get(name=room_name)
        if not room.members.filter(id=user.id).exists():
            return render(request, 'dashboard.html')
        

        messages = Message.objects.filter(room_name = room).order_by('timestamp')
        message_contents = decrypted_history_msg(messages)
        is_group = True

        members_list = []

        for member in room.members.all():
            members_list.append(member.username)

        members_name = " & ".join(members_list)

    except ChatRoom.DoesNotExist:

        user_ids = room_name.split('_')

        if str(user.id) not in user_ids:
            return render(request, "dashboard.html")

        members_list = []

        for member_id in user_ids:
            try:
                member = User.objects.get(id=int(member_id))

                if not member.id == user.id:
                    members_list.append(member.username)            

            except User.DoesNotExist:
                return redirect('dashboard')
        
        members_name = " & ".join(members_list)

        messages = Message.objects.filter(room_name=room_name).order_by("timestamp")

        message_contents = decrypted_history_msg(messages)
        room = None
        is_group = False
        
    return render(request, 'chat.html', {
        'room_name': room_name,
        'room_member': members_name,
        'messages': message_contents,
        'is_group': is_group,
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
        "user_rooms": user_rooms,
        "all_users": users,
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

        return redirect("chat_room", room_name=room.name)