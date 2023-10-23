from enum import Enum
import logging
import copy

from .utils import gen_password, AppUtilException
from .answerer import Answerer, AnswererStatus
from .kvs import KVS, KeyGroupName
from mysite.config import MyConfig


class RoomStatus(Enum):
    CREATING = 1
    WAITING = 2
    ASKING = 3
    ANSWERING = 4
class Room:
    def __init__(self):
        self.name = None
        self.password = gen_password(MyConfig.App.SIZE_PASSWORD)
        self.status = RoomStatus.CREATING.value
        self.question_no = 0

# FIXME:全体的に排他制御必要。get_objにfor_update = Noneとか作って、ロックかけるか。ß
class RoomUtil:
    @staticmethod
    def get(room_id):
        room = KVS.get_obj(KeyGroupName.ROOM + room_id)
        if room is None:
            raise AppUtilException("部屋が存在しない")
        return room

    @staticmethod
    def check_password(room_id, password):
        room = KVS.get_obj(KeyGroupName.ROOM + room_id)
        if room.password == password:
            pass
        else:
            raise AppUtilException("パスワード不一致")
        
    @staticmethod
    def add_answerer(room_id, name):
        if (name is None) or (name == ""):
            raise AppUtilException("解答者名が不正")

        answerers = KVS.get_hash_obj(KeyGroupName.ANSERERS + room_id)
        for answerer in answerers.values():
            if answerer.name == name:
                raise AppUtilException("解答者名が重複")

        digit_answerer_id = len(str(MyConfig.App.MAX_ANSWERER_ID))
        hkeys = []
        for answerer_id in range(MyConfig.App.MIN_ANSWERER_ID, MyConfig.App.MAX_ANSWERER_ID):
            s_answerer_id = str(answerer_id).zfill(digit_answerer_id)
            hkeys.append(s_answerer_id)

        answerer = Answerer(name)
        hkey = KVS.set_hash_sw_obj(KeyGroupName.ANSERERS + room_id, hkeys, answerer)
        if hkey is not None:
            return hkey
        else:
            raise AppUtilException("参加者ID枯渇")
            
    @staticmethod
    def get_dict(room_id):
        room = KVS.get_obj(KeyGroupName.ROOM + room_id)
        room_dict = copy.deepcopy(vars(room))
        answerer_dicts = []
        answerers = KVS.get_hash_obj(KeyGroupName.ANSERERS + room_id)
        for answerer in answerers.values():
            answerer_dicts.append(copy.deepcopy(vars(answerer)))
        room_dict["answerers"] = answerer_dicts
        return room_dict
    
    @staticmethod
    def question(room_id):
        room = KVS.get_obj(KeyGroupName.ROOM + room_id)
        room.status = RoomStatus.ASKING.value
        room.question_no += 1
        KVS.set_obj(KeyGroupName.ROOM + room_id, room)


    @staticmethod
    def answer(room_id, answerer_name):
        room = KVS.get_obj(KeyGroupName.ROOM + room_id)
        room.status = RoomStatus.ANSWERING.value
        KVS.set_obj(KeyGroupName.ROOM + room_id, room)

        answerers = KVS.get_hash_obj(KeyGroupName.ANSERERS + room_id)
        for answer in answerers.values():
            if answer.status == AnswererStatus.ANSWERING.value:
                return
        for answer_id, answer in answerers.items():
            if answer.name == answerer_name:
                answer.status = AnswererStatus.ANSWERING.value
                KVS.set_hash_obj(KeyGroupName.ANSERERS + room_id, answer_id, answer)
                return

    @staticmethod
    def correct(room_id):
        room = KVS.get_obj(KeyGroupName.ROOM + room_id)
        room.status = RoomStatus.WAITING.value
        KVS.set_obj(KeyGroupName.ROOM + room_id, room)

        answerers = KVS.get_hash_obj(KeyGroupName.ANSERERS + room_id)
        for answer_id, answer in answerers.items():
            if answer.status == AnswererStatus.ANSWERING.value:
                answer.status = AnswererStatus.WAITING.value
                answer.score += 1
                KVS.set_hash_obj(KeyGroupName.ANSERERS + room_id, answer_id, answer)
                return

    @staticmethod
    def incorrect(room_id):
        room = KVS.get_obj(KeyGroupName.ROOM + room_id)
        room.status = RoomStatus.WAITING.value
        KVS.set_obj(KeyGroupName.ROOM + room_id, room)

        answerers = KVS.get_hash_obj(KeyGroupName.ANSERERS + room_id)
        for answer_id, answer in answerers.items():
            if answer.status == AnswererStatus.ANSWERING.value:
                answer.status = AnswererStatus.WAITING.value
                KVS.set_hash_obj(KeyGroupName.ANSERERS + room_id, answer_id, answer)
                return

    @staticmethod
    def issue():
        keys = []
        digit_room_id = len(str(MyConfig.App.MAX_ROOM_ID))
        for room_id in range(MyConfig.App.MIN_ROOM_ID, MyConfig.App.MAX_ROOM_ID):
            s_room_id = str(room_id).zfill(digit_room_id)
            keys.append(KeyGroupName.ROOM + s_room_id)
        
        room = Room()
        key = KVS.set_sw_obj(keys, room)
        if key is not None:
            return (key.replace(KeyGroupName.ROOM, ""), room)
        else:
            raise AppUtilException("ルームID枯渇")
        
    @staticmethod
    def config(room_id, room_name):
        room = KVS.get_obj(KeyGroupName.ROOM + room_id)
        if room.status == RoomStatus.CREATING.value:
            room.name = room_name
            room.status = RoomStatus.WAITING.value
            KVS.set_obj(KeyGroupName.ROOM + room_id, room)
        else:
            raise AppUtilException("部屋ステータス異変")



