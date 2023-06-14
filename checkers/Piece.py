from __future__ import annotations
from .graphics_constants import SQUARE_HEIGHT, SQUARE_WIDTH, PLAYER_TOP_COLOR, PLAYER_BOTTOM_COLOR
from .game_constants import ROWS
from .Player import Player


class Piece:
    def __init__(self, row: int, col: int, player: Player) -> None:
        self.row = row
        self.col = col
        self.player = player
        self.is_queen = False

    def __eq__(self, other: Piece) -> bool:
        if not isinstance(other, Piece):
            return False
        return self.row == other.row and self.col == other.col and \
               self.player == other.player and self.is_queen == other.is_queen

    def __repr__(self) -> str:
        piece_type = 'K' if self.is_queen else 'M'
        player_info = 'TOP' if self.player == Player.PLAYER_TOP else 'BOT'
        representation = str((self.row, self.col)) + '(' + piece_type + '_' + player_info + ')'
        return representation

    @property
    def color(self) -> tuple[int, int, int]:
        if self.player == Player.PLAYER_TOP:
            return PLAYER_TOP_COLOR
        elif self.player == Player.PLAYER_BOTTOM:
            return PLAYER_BOTTOM_COLOR

    @property
    def is_ready_to_promote(self) -> bool:
        if self.is_queen:
            return False
        if self.player == Player.PLAYER_BOTTOM and self.row == 0:
            return True
        if self.player == Player.PLAYER_TOP and self.row == ROWS-1:
            return True
        return False

    @property
    def position_on_display(self) -> tuple[int, int]:
        # Returns center of the square that piece is displayed on
        y = self.row * SQUARE_HEIGHT + SQUARE_HEIGHT//2
        x = self.col * SQUARE_WIDTH + SQUARE_WIDTH//2
        return x, y

    def promote(self) -> None:
        self.is_queen = True

    def move(self, destination_row: int, destination_col: int) -> None:
        self.row = destination_row
        self.col = destination_col

    def is_rival_piece(self, piece: Piece) -> bool:
        return self.player != piece.player


