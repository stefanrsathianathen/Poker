from enum import Enum,auto

class ACTION(Enum):
    BET = auto()
    CALL = auto()
    CHECK = auto()
    ALLIN = auto()
    FOLD = auto()

class ROUNDSTATUS(Enum):
    IN_ROUND = auto()
    FINISH = auto()
    FOLD = auto()

class BETTINGSTATUS(Enum):
    BETTING = auto()
    READY = auto()

class HANDRANK(Enum):
    ROYAL_FLUSH = (10, "Royal Flush")
    STRAIGHT_FLUSH = (9, "Straight Flush")
    FOUR_OF_A_KIND = (8, "Four of a Kind")
    FULL_HOUSE = (7, "Full House")
    FLUSH = (6, "Flush")
    STRAIGHT = (5, "Straight")
    THREE_OF_A_KIND = (4, "Three of a Kind")
    TWO_PAIR = (3, "Two Pair")
    PAIR = (2, "Pair")
    HIGH_CARD = (1, "High Card")
    NOTHING = (0, "NOTHING")

    def __lt__(self, value):
        if self.__class__ is value.__class__:
            return self.value[0] < value.value[0]
        return NotImplemented
