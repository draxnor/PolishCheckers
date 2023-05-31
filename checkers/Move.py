from .Piece import Piece


class Move:
    def __init__(self, start_row, start_col, target_row, target_col, captured_piece: Piece = None):
        self.start_row = start_row
        self.start_col = start_col
        self.target_row = target_row
        self.target_col = target_col
        self.captured_piece = captured_piece

    def __repr__(self):
        repr_str = 'From:' + str((self.start_row, self.start_col)) + \
        ' To:' + str((self.target_row, self.target_col)) + \
        ', capturing: ' + str(self.captured_piece)
        return repr_str

    def __eq__(self, other):
        return self.start_row == other.start_row and self.start_col == other.start_col and \
               self.target_row == other.target_row and self.target_col == other.target_col and \
               self.captured_piece.row == other.captured_piece.row and \
               self.captured_piece.col == other.captured_piece.col and \
               self.captured_piece.player == other.captured_piece.player

    @property
    def destination(self):
        return self.target_row, self.target_col


# class MoveSequence:
#      def __init__(self):
#         current_move