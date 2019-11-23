from enum import Enum,auto

class ACTION(Enum):
    BET = auto()
    CALL = auto()
    FOLD = auto()

class ROUNDSTATUS(Enum):
    IN_ROUND = auto()
    FINISH = auto()
    FOLD = auto()

class BETTINGSTATUS(Enum):
    BETTING = auto()
    READY = auto()