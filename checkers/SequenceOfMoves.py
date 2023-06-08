from .Piece import Piece
from .Move import Move

class SequenceOfMoves:
    def __init__(self, piece: Piece, sequence_as_list: list = []):
        self.moving_piece = piece
        self._sequence = sequence_as_list

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
        captured_pieces = []
        for move in self._sequence:
            if move.captured_piece is not None:
                captured_pieces.append(move.captured_piece)

        return captured_pieces
