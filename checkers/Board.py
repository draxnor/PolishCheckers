import pygame
from .constants import *
from .Piece import Piece
from .Player import Player
from .Move import Move

class Board():
    def __init__(self):
        self.board = []
        self.create_board()
        self.player1_men_left = self.player2_men_left = 20
        self.player1_kings_left = self.player2_kings_left = 0

    def draw_board(self,window):
        self.draw_background(window)
        self.draw_pieces(window)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS-1 or row == 0:
            piece.promote_piece()
            if piece.player == Player.PLAYER_TOP:
                self.player1_kings_left += 1
            elif piece.player == Player.PLAYER_BOTTOM:
                self.player2_kings_left += 1

    @staticmethod
    def draw_background(window):
        window.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLUMNS):
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                    pygame.draw.rect(window, WHITE,
                                     pygame.Rect((row*SQUARE_WIDTH, col*SQUARE_HEIGHT), (SQUARE_WIDTH, SQUARE_HEIGHT)))

    def draw_pieces(self, window):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if isinstance(self.board[row][col], Piece):
                    self.board[row][col].draw(window)


    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLUMNS):
                if (row % 2 + col % 2) == 1:
                    if row < 4:
                        self.board[row].append(Piece(row, col, Player.PLAYER_TOP))
                    elif row > 5:
                        self.board[row].append(Piece(row, col, Player.PLAYER_BOTTOM))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(-1)

    def get_piece(self, row, col):
        # if not isinstance(self.board[row][col], Piece):
        #     raise IndexError('There is no piece at passed index.')
        return self.board[row][col]

    def get_valid_moves_of_piece(self, piece: Piece):
        # look for captures first
        # if capture possible, leave only those with the highest possible capture count
        # if captures impossible, leave only normal moves
        if piece.is_king:
            moves = self.get_possible_captures_for_king(piece, piece.row, piece.col)
            if not moves:
                moves = self.get_possible_noncapture_moves_for_king(piece)
        else:
            moves = self.get_possible_captures_for_man_from_field(piece, piece.row, piece.col)
            if not moves:
                moves = self.get_possible_noncapture_moves_for_man(piece)
        return moves

    def get_possible_noncapture_moves_for_man(self, piece: Piece) -> list[Move]:
        list_of_moves = []
        left_col = piece.col - 1
        right_col = piece.col + 1
        if piece.player == Player.PLAYER_TOP:
            target_row = piece.row + 1
        else: # piece.player == Player.PLAYER_BOTTOM:
            target_row = piece.row - 1
        if 0 <= target_row < ROWS:
            if 0 <= left_col:
                if self.board[target_row][left_col] == 0:
                    list_of_moves.append([Move(piece.row, piece.col, target_row, left_col)])
            if right_col < COLUMNS:
                if self.board[target_row][right_col] == 0:
                    list_of_moves.append([Move(piece.row, piece.col, target_row, right_col)])
        return list_of_moves

    def _is_out_of_bound(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLUMNS:
            return False
        return True

    def get_possible_captures_for_man_from_field(self, piece, row, col, captured_pieces=[]):
        possible_sequences = []
        # for every diagonal
        for horizontal_step in (-1, 1):
            for vertical_step in (-1, 1):
                row_after_capture = row+2*vertical_step
                col_after_capture = col+2*horizontal_step
                # if there is a space (2 fields) for capture in that direction
                if not self._is_out_of_bound(row_after_capture, col_after_capture):
                    neighboring_field_content = self.get_piece(row+vertical_step, col+horizontal_step)
                    # if field next to piece is a piece,
                    # belongs to opponent and was not already captured in current sequence
                    if isinstance(neighboring_field_content, Piece):
                        if neighboring_field_content.is_rival_piece(piece) and \
                                neighboring_field_content not in captured_pieces:
                            field_behind_rival_piece_content = self.get_piece(row_after_capture, col_after_capture)
                            # if field behind rival piece is empty or would be empty after moving current piece
                            # (can happen after multiple captures)
                            if field_behind_rival_piece_content == 0 or field_behind_rival_piece_content == piece:
                                # copy list and add element
                                current_move = Move(row, col, row_after_capture, col_after_capture, neighboring_field_content)
                                # copy list as original list is needed for next loop iteration,
                                # add freshly captured piece to list
                                captured_pieces_updated = captured_pieces + [neighboring_field_content]
                                # pass list of captured pieces in a current sequence
                                # including one made in that iteration
                                continuation_sequences = self.get_possible_captures_for_man_from_field\
                                    (piece, row_after_capture, col_after_capture, captured_pieces_updated)

                                if not continuation_sequences:
                                    possible_sequences.append([current_move])
                                else:
                                    for seq in continuation_sequences:
                                        seq.append(current_move)
                                        possible_sequences.append(seq)
        return possible_sequences

    def get_possible_captures_for_king(self, piece, row, col, captured_pieces=[]):
        possible_sequences = []
        # for every diagonal
        for horizontal_step in (-1, 1):
            for vertical_step in (-1, 1):
                row_examined = row + vertical_step
                col_examined = col + horizontal_step
                while 0 < row_examined < ROWS-1 and 0 < col_examined < COLUMNS-1:
                    field_content = self.get_piece(row_examined, col_examined)
                    if not isinstance(field_content, Piece):
                        continue
                    if not field_content.is_rival_piece(piece):
                        break
                    field_behind_rival_piece_content = \
                        self.get_piece(row_examined + vertical_step, col_examined + horizontal_step)
                    if field_behind_rival_piece_content != 0:
                        break
                    # it is rival piece on diagonal and there is at least 1 free field behind piece,
                    # it means that piece capturing is possible

                    # TODO
                    # Follow idea from function 'get_possible_captures_for_man_from_field'
                    # current_move = Move(row, col, row_after_capture, col_after_capture, neighboring_field_content)
                    # captured_pieces_updated = captured_pieces + [neighboring_field_content]
                    # continuation_sequences = self.get_possible_captures_for_man_from_field\
                    #     (piece, row_after_capture, col_after_capture, captured_pieces_updated)
                    #
                    # if not continuation_sequences:
                    #     possible_sequences.append([current_move])
                    # else:
                    #     for seq in continuation_sequences:
                    #         seq.append(current_move)
                    #         possible_sequences.append(seq)
                    row_examined += vertical_step
                    col_examined += horizontal_step
        return possible_sequences

    def get_possible_noncapture_moves_for_king(self, piece: Piece):
        #TODO
        return []

    def highlight_square(self, window, row, col):
        assert(self.board[row][col] == 0, 'Error in highlighting square: square not empty.')
        pygame.draw.rect(window, HIGHLIGHT_COLOR,
                         pygame.Rect((col * SQUARE_WIDTH, row * SQUARE_HEIGHT), (SQUARE_WIDTH, SQUARE_HEIGHT)))
