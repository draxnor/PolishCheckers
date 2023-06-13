from .Piece import Piece
from .Move import Move


class SequenceOfMoves:
    def __init__(self, piece: Piece, sequence_as_list: list = []):
        self.moving_piece = piece
        self._sequence = sequence_as_list

    def __eq__(self, other):
        if not isinstance(other, SequenceOfMoves):
            return False
        if not self.length == other.length:
            return False
        for move_from_self, move_from_other in zip(self.sequence, other.sequence):
            if not move_from_self == move_from_other:
                return False
        if not self.moving_piece == other.moving_piece:
            return False
        return True

    def __repr__(self):
        header = f'Sequence contains {self.length} moves:'
        moves_description = '\n'.join([str(move) for move in self._sequence])
        return header + '\n' + moves_description + '\n'

    @property
    def first_move(self):
        if self._sequence:
            return self._sequence[-1]

    @property
    def sequence(self):
        return self._sequence

    @property
    def length(self):
        return len(self._sequence)

    @property
    def captured_pieces(self):
        return [move for move in self._sequence if move.captured_piece is not None]

    def pop(self):
        return self._sequence.pop()

    def add_next_move(self, move: Move):
        self._sequence.insert(0, move)

    def add_previous_move(self, move: Move):
        self._sequence.append(move)

    def does_contain_capturing(self):
        return any([move.does_contain_capture() for move in self._sequence])

    def get_moving_piece(self):
        return self.moving_piece

    def draw_sequence(self, window):
        for move in self._sequence:
            move.draw_move_destination_as_distant_move(window)

    def draw_move_in_sequence_as_next_move(self, window, position = 0):
        self._sequence[-position-1].draw_move_destination_as_closest_move(window)

    def is_empty(self):
        return self.length == 0

    def set_sequence_from_list(self, sequence_as_list: list):
        self._sequence = sequence_as_list