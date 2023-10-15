from enum import Enum
import logging
import copy

from .utils import gen_password, AppUtilException
from .answerer import Answerer, AnswererStatus

rooms = {}

class RoomStatus(Enum):
    CREATING = 1
    WAITING = 2
    ASKING = 3
    ANSWERING = 4

class Room:
    __MIN_ROOM_ID = 1
    __MAX_ROOM_ID = 999
    __SIZE_PASSWORD = 6

    def __init__(self):
        self.id = self.__issue_room_id()
        self.name = None
        self.password = gen_password(self.__SIZE_PASSWORD)
        self.status = RoomStatus.CREATING.value
        self.answerers = []
        self.question_no = 0

    @staticmethod
    def get_instance(room_id):
        room = rooms.get(room_id)
        if room is None:
            raise AppUtilException("ルームが存在しない")
        return room
    
    def is_password_ok(self, password):
        if self.password == password:
            return True
        else:
            return False
        
    def add_answerer(self, name):
        for answerer in self.answerers:
            if answerer.name == name:
                raise AppUtilException("解答者名が重複")
        
        answerer = Answerer(name)
        self.answerers.append(answerer)
    
    def to_dict(self):
        self_dict = copy.deepcopy(vars(self))
        answerer_dicts = []
        for answerer in self.answerers:
            answerer_dicts.append(copy.deepcopy(vars(answerer)))
        self_dict["answerers"] = answerer_dicts
        return self_dict
    
    def question(self):
        self.status = RoomStatus.ASKING.value
        self.question_no += 1

    def answer(self, answerer_name):
        self.status = RoomStatus.ANSWERING.value

        for answer in self.answerers:
            if answer.status == AnswererStatus.ANSWERING.value:
                return
        
        for answer in self.answerers:
            if answer.name == answerer_name:
                answer.status = AnswererStatus.ANSWERING.value
                return

    def correct(self):
        self.status = RoomStatus.WAITING.value

        for answer in self.answerers:
            if answer.status == AnswererStatus.ANSWERING.value:
                answer.status = AnswererStatus.WAITING.value
                answer.score += 1
                return

    def incorrect(self):
        self.status = RoomStatus.WAITING.value

        for answer in self.answerers:
            if answer.status == AnswererStatus.ANSWERING.value:
                answer.status = AnswererStatus.WAITING.value
                return

    def __issue_room_id(self):
        global rooms

        digit_room_id = len(str(self.__MAX_ROOM_ID))
        for room_id in range(self.__MIN_ROOM_ID, self.__MAX_ROOM_ID):
            s_room_id = str(room_id).zfill(digit_room_id)
            if s_room_id not in rooms.keys():
                rooms[s_room_id] = self
                return s_room_id
        raise AppUtilException("ルームID枯渇")
    

    
