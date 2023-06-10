import  pygame
from .Piece import Piece
from .Move import Move

class SequenceOfMoves:
    def __init__(self, piece: Piece, sequence_as_list: list = []):
        self.moving_piece = piece
        self._sequence = sequence_as_list

    @property
    def first_move(self):
        if self._sequence:
            return self.sequence[-1]

    def pop(self):
        return self._sequence.pop()

    def add_next_move(self, move: Move):
        self._sequence.insert(0, move)

    def add_previous_move(self, move: Move):
        self._sequence.append(move)

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence_as_list: list):
        self._sequence = sequence_as_list

    @property
    def length(self):
        return len(self._sequence)

    @property
    def captured_pieces(self):
        return [move for move in self._sequence if move.captured_piece is not None]

    def does_contain_capturing(self):
        return any([move.does_contain_capture() for move in self._sequence])

    def get_moving_piece(self):
        return self.moving_piece

    def __repr__(self):
        header = f'Sequence contains {self.length} moves:'
        moves_description = '\n'.join([str(move) for move in self._sequence])
        return header + '\n' + moves_description + '\n'

    def draw_sequence(self, window):
        for move in self._sequence:
            move.draw_move_destination_as_distant_move(window)

    def draw_move_in_sequence_as_closest(self, window, position):
        self._sequence[-position-1].draw_move_destination_as_closest_move(window)

    def is_empty(self):
        return self.length == 0

