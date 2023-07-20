from __future__ import annotations
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

    def copy(self):
        cls = self.__class__
        new_piece = cls.__new__(cls)
        new_piece.__dict__.update(self.__dict__)
        new_piece.row = self.row
        new_piece.col = self.col
        new_piece.player = self.player
        new_piece.is_queen = self.is_queen
        return new_piece

    @property
    def is_ready_to_promote(self) -> bool:
        if self.is_queen:
            return False
        if self.player == Player.PLAYER_BOTTOM and self.row == 0:
            return True
        if self.player == Player.PLAYER_TOP and self.row == ROWS-1:
            return True
        return False

    def promote(self) -> None:
        self.is_queen = True

    def move(self, destination_row: int, destination_col: int) -> None:
        self.row = destination_row
        self.col = destination_col

    def is_rival_piece(self, piece: Piece) -> bool:
        return self.player != piece.player


