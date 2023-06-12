from enum import Enum, auto


class GameState(Enum):
    ONGOING = auto()
    PLAYER_TOP_WON = auto()
    PLAYER_BOTTOM_WON = auto()
    DRAW = auto()
