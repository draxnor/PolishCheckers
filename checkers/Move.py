from .Piece import Piece


#TODO
class Move:
    def __init__(self, start_row, start_col, target_row, target_col, captured_piece: Piece = None):
        self.origin_row = start_row
        self.origin_col = start_col
        self.destination_row = target_row
        self.destination_col = target_col
        self.captured_piece = captured_piece

    def __repr__(self):
        repr_str = 'From:' + str((self.origin_row, self.origin_col)) + \
        ' To:' + str((self.destination_row, self.destination_col)) + \
        ', capturing: ' + str(self.captured_piece)
        return repr_str

    def __eq__(self, other):
        return self.origin_row == other.origin_row and self.origin_col == other.origin_col and \
               self.destination_row == other.destination_row and self.destination_col == other.destination_col and \
               self.captured_piece.row == other.captured_piece.row and \
               self.captured_piece.col == other.captured_piece.col and \
               self.captured_piece.player == other.captured_piece.player

    @property
    def destination(self):
        return self.destination_row, self.destination_col

    @property
    def origin(self):
        return self.origin_row, self.origin_col
