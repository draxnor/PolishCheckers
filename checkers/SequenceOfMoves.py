from __future__ import annotations

import pygame

from .Piece import Piece
from .Move import Move


class SequenceOfMoves:
    def __init__(self, piece: Piece, sequence_as_list: list[Move] = []) -> None:
        self._moving_piece = piece
        self._sequence = sequence_as_list

    def __eq__(self, other: SequenceOfMoves) -> bool:
        if not isinstance(other, SequenceOfMoves):
            return False
        if not self.length == other.length:
            return False
        for move_from_self, move_from_other in zip(self.sequence, other.sequence):
            if not move_from_self == move_from_other:
                return False
        if not self._moving_piece == other._moving_piece:
            return False
        return True

    def __repr__(self) -> str:
        header = f'Sequence contains {self.length} moves:'
        moves_description = '\n'.join([str(move) for move in self._sequence])
        return header + '\n' + moves_description + '\n'

    @property
    def first_move(self) -> Move:
        if self._sequence:
            return self._sequence[-1]

    @property
    def sequence(self) -> list[Move]:
        return self._sequence

    @property
    def length(self) -> int:
        return len(self._sequence)

    @property
    def moving_piece(self) -> Piece:
        return self._moving_piece

    @property
    def captured_pieces(self) -> []:
        return [move.captured_piece for move in self._sequence if move.captured_piece is not None]

    def pop(self) -> Move:
        return self._sequence.pop()

    def add_next_move(self, move: Move) -> None:
        self._sequence.insert(0, move)

    def add_previous_move(self, move: Move) -> None:
        self._sequence.append(move)

    def does_contain_capturing(self) -> bool:
        return any([move.does_contain_capture() for move in self._sequence])

    def draw_sequence(self, window: pygame.Surface) -> None:
        for move in self._sequence:
            move.draw_move_destination_as_distant_move(window)

    def draw_move_in_sequence_as_next_move(self, window: pygame.Surface, position: int = 0) -> None:
        self._sequence[-position-1].draw_move_destination_as_closest_move(window)

    def is_empty(self) -> bool:
        return self.length == 0

    def set_sequence_from_list(self, sequence_as_list: list[Move] = []):
        self._sequence = [move for move in sequence_as_list]