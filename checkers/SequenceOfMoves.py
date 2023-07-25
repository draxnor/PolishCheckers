from __future__ import annotations

import sys

from .Piece import Piece
from .Move import Move


class SequenceOfMoves:
    def __init__(self, moving_piece: Piece, sequence_as_list: list[Move] = None) -> None:
        if sequence_as_list is None:
            sequence_as_list = []
        self._moving_piece = moving_piece
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
        moves_description = '\n'.join([str(move) for move in self._sequence[::-1]])
        return header + '\n' + moves_description + '\n'

    @property
    def first_move(self) -> Move:
        if self._sequence:
            return self._sequence[-1]

    @property
    def last_move(self) -> Move:
        if self._sequence:
            return self._sequence[0]

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

    def is_empty(self) -> bool:
        return self.length == 0

    def set_sequence_from_list(self, sequence_as_list: list[Move]):
        if sequence_as_list is None:
            print('Trying to initialize SequenceOfMoves from empty list.', file=sys.stderr)
            raise Exception("Initializing SequenceOfMoves from empty list of moves.")
        self._sequence = [move for move in sequence_as_list]
        self._moving_piece = sequence_as_list[0].moving_piece

    def clear_sequence(self):
        self._moving_piece = None
        self._sequence.clear()
