from django.shortcuts import render
from .room import RoomUtil, RoomStatus
from .utils import AppUtilException
import logging

# Create your views here.
def index(request):
    return render(request, "chat/index.html")

def room_creation(request):
    (room_id, trg_room) = RoomUtil.issue()
    return render(request, "chat/room-creation.html",{
        "room_id": room_id,
        "room_pw": trg_room.password
    })

def room_entering(request):
    return render(request, "chat/room-entering.html")

def room_questioner(request, room_id):
    p_room_id = None
    room_pw = None
    room_name = None
    if request.method == "POST":
        p_room_id = request.POST.get('room-id')
        room_pw = request.POST.get('room-pw')
        room_name = request.POST.get('room-name')

        RoomUtil.check_password(p_room_id, room_pw)
        RoomUtil.config(p_room_id, room_name)
    else:
        raise AppUtilException("HTTPメソッド不一致")
        
    return render(request, "chat/room-questioner.html", {
        "room_id": p_room_id,
        "room_pw": room_pw,
        "room_name": room_name
    })

def room_answerer(request, room_id):
    p_room_id = None
    room_pw = None
    room_name = None
    answerer_name = None
    if request.method == "POST":
        p_room_id = request.POST.get('room-id')
        room_pw = request.POST.get('room-pw')
        answerer_name = request.POST.get('answerer-name')

        RoomUtil.check_password(p_room_id, room_pw)
        RoomUtil.add_answerer(p_room_id, answerer_name)
        trg_room = RoomUtil.get(p_room_id)
        room_name = trg_room.name
    else:
        raise AppUtilException("HTTPメソッド不一致")

    return render(request, "chat/room-answerer.html", {
        "room_id": p_room_id,
        "room_pw": room_pw,
        "room_name": room_name,
        "answerer_name": answerer_name
    })
