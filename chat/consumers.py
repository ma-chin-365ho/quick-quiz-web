import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from .utils import AppUtilException
from .room import RoomUtil


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        room_id = text_data_json["roomId"]
        room_pw = text_data_json["roomPw"]
        name = text_data_json["name"]
        msg = text_data_json["msg"]

        RoomUtil.check_password(room_id, room_pw)

        if msg == "question":
            RoomUtil.question(room_id)
        elif msg == "answer":
            RoomUtil.answer(room_id, name)
        elif msg == "correct":
            RoomUtil.correct(room_id)
        elif msg == "incorrect":
            RoomUtil.incorrect(room_id)
        elif msg == "ping":
            pass

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "room_id": room_id}
        )

    # Receive message from room group
    async def chat_message(self, event):
        room_id = event["room_id"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps(RoomUtil.get_dict(room_id)))