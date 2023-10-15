from django.shortcuts import render
from .room import Room, RoomStatus
from .utils import AppUtilException
import logging

# Create your views here.
def index(request):
    return render(request, "chat/index.html")

def room_creation(request):
    trg_room = Room()
    return render(request, "chat/room-creation.html",{
        "room_id": trg_room.id,
        "room_pw": trg_room.password
    })

def room_entering(request):
    return render(request, "chat/room-entering.html")

def room_questioner(request, room_id):
    if request.method == "POST":
        p_room_id = request.POST.get('room-id')
        room_pw = request.POST.get('room-pw')
        room_name = request.POST.get('room-name')

        if (
            p_room_id is not None and
            room_pw is not None and
            room_name is not None
        ):
            trg_room = Room.get_instance(p_room_id)
            if trg_room.is_password_ok(room_pw):
                if trg_room.status == RoomStatus.CREATING.value:
                    trg_room.name = room_name
                    trg_room.status = RoomStatus.WAITING.value
            else:
                raise AppUtilException("パスワード不一致")
                pass
    return render(request, "chat/room-questioner.html", {
        "room_id": trg_room.id,
        "room_pw": trg_room.password,
        "room_name": trg_room.name
    })

def room_answerer(request, room_id):
    if request.method == "POST":
        p_room_id = request.POST.get('room-id')
        room_pw = request.POST.get('room-pw')
        answerer_name = request.POST.get('answerer-name')

        if (
            p_room_id is not None and
            room_pw is not None and
            answerer_name is not None
        ):
            trg_room = Room.get_instance(p_room_id)
            if trg_room.is_password_ok(room_pw):
                trg_room.add_answerer(answerer_name)
            else:
                raise AppUtilException("パスワード不一致")
                pass
    return render(request, "chat/room-answerer.html", {
        "room_id": trg_room.id,
        "room_pw": trg_room.password,
        "room_name": trg_room.name,
        "answerer_name": answerer_name
    })
