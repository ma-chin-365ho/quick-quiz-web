import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from .utils import AppUtilException
from .room import Room, RoomStatus


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

        trg_room = Room.get_instance(room_id)

        if not trg_room.is_password_ok(room_pw):
            raise AppUtilException("パスワード不一致")

        if msg == "question":
            trg_room.question()
        elif msg == "answer":
            trg_room.answer(name)
        elif msg == "correct":
            trg_room.correct()
        elif msg == "incorrect":
            trg_room.incorrect()
        elif msg == "ping":
            pass

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "room_id": room_id}
        )

    # Receive message from room group
    async def chat_message(self, event):
        room_id = event["room_id"]
        trg_room = Room.get_instance(room_id)

        # Send message to WebSocket
        logging.error(trg_room.to_dict())
        await self.send(text_data=json.dumps(trg_room.to_dict()))