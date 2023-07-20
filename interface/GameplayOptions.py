from checkers.Player import Player
from enum import Enum, auto


class PlayerSide(Enum):
    TOP = auto()
    BOTTOM = auto()


class PlayerType(Enum):
    Human = auto()
    AI = auto()


class GameplayOptions:
    def __init__(self,
                 starting_side: PlayerSide = PlayerSide.TOP,
                 top_player_type: PlayerType = PlayerType.Human,
                 bottom_player_type: PlayerType = PlayerType.Human,
                 top_ai_depth: int = 4,
                 bottom_ai_depth: int = 4):

        self._starting_side = starting_side
        self._top_player_type = top_player_type
        self._bottom_player_type = bottom_player_type
        self._top_ai_depth = top_ai_depth
        self._bottom_ai_depth = bottom_ai_depth

    @property
    def starting_side(self):
        return self._starting_side

    @property
    def top_player_type(self):
        return self._top_player_type

    @property
    def bottom_player_type(self):
        return self._bottom_player_type

    @property
    def top_ai_depth(self):
        if self.top_player_type == PlayerType.AI:
            return self._top_ai_depth
        else:
            return 0

    @property
    def bottom_ai_depth(self):
        if self.bottom_player_type == PlayerType.AI:
            return self._bottom_ai_depth
        else:
            return 0

    def set_starting_side(self, side: PlayerSide) -> None:
        self._starting_side = side

    def set_top_player_type(self, player_type: PlayerType) -> None:
        self._top_player_type = player_type

    def set_bottom_player_type(self, player_type: PlayerType) -> None:
        self._bottom_player_type = player_type

    def set_top_ai_depth(self, ai_depth: int) -> None:
        self._top_ai_depth = ai_depth

    def set_bottom_ai_depth(self, ai_depth: int) -> None:
        self._bottom_ai_depth = ai_depth



