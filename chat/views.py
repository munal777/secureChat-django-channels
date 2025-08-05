import re

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from urllib.parse import unquote, quote

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
        
        messages = Message.objects.filter(room_name = room.name).order_by('timestamp')

        message_contents = decrypted_history_msg(messages)
        is_group = True

        members_list = []

        for member in room.members.all():
            members_list.append(member.username)
        
        members_num = len(members_list)

        members_name = None

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
        members_num = None
    
    print(f"room name in chat: {room_name}")
        
    return render(request, 'chat.html', {
        'room_name': room_name,
        'room_member': members_name,
        'members_list': members_list,
        'messages': message_contents,
        'is_group': is_group,
        'members_num': members_num,
    })


@login_required
def dashboard_view(request):
    current_user = request.user
    users = User.objects.exclude(id=request.user.id)
    group_rooms = ChatRoom.objects.filter(members=request.user, is_group=True)

    user_rooms = [
        {
            "username": user.username,
            "room_name": make_room_name(current_user.id, user.id),
        }
        for user in users
    ]

    return render(request, "dashboard.html", {
        "user_rooms": user_rooms,
        "all_users": users,
        "group_rooms": group_rooms,
        "current_user": current_user,
    })



def landing_page_view(request):
    return render(request, 'landing.html')


@login_required
def create_group_view(request):
    if request.method == "POST":
        raw_group_name = request.POST["room_name"].strip()

        group_name = re.sub(r'\s+', ' ', raw_group_name)

        # Check valid characters: letters, numbers, space, underscore, dash
        if not re.fullmatch(r'[A-Za-z0-9 _-]+', group_name):
            messages.error(request, "Group name can only contain letters, numbers, spaces, underscores, or dashes.")
            return redirect("dashboard")

        # Ensure group name contains at least one letter or number
        if not re.search(r'[A-Za-z0-9]', group_name):
            messages.error(request, "Group name must include at least one letter or number.")
            return redirect("dashboard")

        member_ids = request.POST.getlist("members")

        if not ChatRoom.objects.filter(name=group_name).exists():
            room = ChatRoom.objects.create(name=group_name, is_group=True)
            room.members.set(User.objects.filter(id__in = member_ids))
            room.members.add(request.user)
            room.save()

            return redirect("chat_room", room_name=room.name)
        
        messages.error(request, "The enter room name already exists.")
        return redirect("dashboard")
    

@login_required
def leave_group_view(request):
    if request.method == "POST":
        group_name = request.POST["room_name"]
        user = request.user
        
        print(group_name)

        try:
            room = ChatRoom.objects.get(name=group_name, is_group=True)
            room.members.remove(user)
        except ChatRoom.DoesNotExist:
             print("Group does not exist.")
        
        return redirect('dashboard')


    

