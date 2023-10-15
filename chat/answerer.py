from enum import Enum

class AnswererStatus(Enum):
    WAITING = 1
    ANSWERING = 2

class Answerer:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.status = AnswererStatus.WAITING.value
