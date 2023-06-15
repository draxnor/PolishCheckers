from __future__ import annotations
from .Piece import Piece


class Move:
    def __init__(self, moving_piece: Piece, start_row: int, start_col: int,
                 target_row: int, target_col: int, captured_piece: Piece = None) -> None:
        self.origin_row = start_row
        self.origin_col = start_col
        self.destination_row = target_row
        self.destination_col = target_col
        self._moving_piece = moving_piece
        self._captured_piece = captured_piece

    def __repr__(self) -> str:
        repr_str = '|' + \
                   'Piece:' + str(self._moving_piece) + ' '\
                   'From:' + str((self.origin_row, self.origin_col)) + ' ' \
                   'To:' + str((self.destination_row, self.destination_col)) + ' ,' \
                   'capturing: ' + str(self.captured_piece) + \
                   '|'
        return repr_str

    def __eq__(self, other: Move) -> bool:
        return self.is_same_origin_and_destination(other) and \
               self.moving_piece == other.moving_piece and \
               self.captured_piece == other.captured_piece

    def is_same_origin_and_destination(self, other: Move) -> bool:
        return self.moving_piece == other.moving_piece and \
               self.origin_row == other.origin_row and \
               self.origin_col == other.origin_col and \
               self.destination_row == other.destination_row and \
               self.destination_col == other.destination_col

    @property
    def moving_piece(self) -> Piece:
        return self._moving_piece

    @property
    def captured_piece(self) -> Piece | None:
        return self._captured_piece

    @property
    def destination(self) -> tuple[int, int]:
        return self.destination_row, self.destination_col

    @property
    def origin(self) -> tuple[int, int]:
        return self.origin_row, self.origin_col

    def does_contain_capture(self) -> bool:
        return self.captured_piece is not None

