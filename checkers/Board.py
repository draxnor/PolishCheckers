import pygame
from .constants import *
from .Piece import Piece
from .Player import Player
from .Move import Move
from .SequenceOfMoves import SequenceOfMoves

class Board():
    def __init__(self):
        self.board = []
        self.create_board()
        self.player1_men_left = self.player2_men_left = 20
        self.player1_kings_left = self.player2_kings_left = 0

    def draw_board(self,window):
        self.draw_background(window)
        self.draw_pieces(window)

    def move(self, move: Move):
        origin_row, origin_col = move.origin
        piece = self.board[origin_row][origin_col]
        destination_row, destination_col = move.destination
        self.board[destination_row][destination_col] = piece
        self.board[origin_row][origin_col] = 0
        piece.move(destination_row, destination_col)

        if destination_row == ROWS-1 and piece.player == Player.PLAYER_TOP and not piece.is_king:
            piece.promote_piece()
            self.player1_kings_left += 1
            self.player1_men_left -= 1
        if destination_row == 0 and piece.player == Player.PLAYER_BOTTOM and not piece.is_king:
            piece.promote_piece()
            self.player2_kings_left += 1
            self.player2_men_left -= 1

    @staticmethod
    def draw_square(row, col, color, window):
        pygame.draw.rect(window, color, pygame.Rect((col*SQUARE_WIDTH, row*SQUARE_HEIGHT), (SQUARE_WIDTH, SQUARE_HEIGHT)))

    @staticmethod
    def draw_background(window):
        window.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLUMNS):
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                    Board.draw_square(row, col, WHITE, window)

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

    def _is_out_of_bound(self, row, col) -> bool:
        if 0 <= row < ROWS and 0 <= col < COLUMNS:
            return False
        return True

    def get_piece(self, row, col):
        assert(not self._is_out_of_bound(row, col), 'Error in getting piece: Index out of bound.')
        return self.board[row][col]

    def get_potential_sequences_for_all_pieces(self, player: Player):
        potential_sequences = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self.board[row][col]
                if isinstance(piece, Piece):
                    if piece.player == player:
                        potential_sequences += self.get_potential_sequences_for_piece(piece)
        return potential_sequences

    def _get_valid_moves_for_a_piece(self, piece: Piece): # not recommended to use because of low speed
        valid_moves = self.get_valid_moves(piece.player)
        return [sequence for sequence in valid_moves if sequence.get_moving_piece() == piece]

    def get_valid_moves(self, player: Player):
        potential_sequences = self.get_potential_sequences_for_all_pieces(player)
        if not potential_sequences:
            return potential_sequences

        max_sequence_length = max([sequence.length for sequence in potential_sequences])
        if max_sequence_length == 1:
            single_capture_sequences = [sequence for sequence in potential_sequences if sequence.does_contain_capturing()]
            if single_capture_sequences:
                return single_capture_sequences
            else:
                return potential_sequences
        else:
            return [sequence for sequence in potential_sequences if sequence.length == max_sequence_length]

    def get_potential_sequences_for_piece(self, piece: Piece):
        # Look for captures first. If captures possible, leave only those with the highest possible capture count
        # If captures impossible, leave only non-capture moves
        if piece.is_queen:
            moves = self.get_potential_capture_sequences_for_queen(piece, piece.row, piece.col)
            if not moves:
                moves = self.get_potential_noncapture_sequences_for_queen(piece)
        else:
            moves = self.get_potential_capture_sequences_for_man(piece, piece.row, piece.col)
            if not moves:
                moves = self.get_potential_noncapture_sequences_for_man(piece)
        if moves:
            max_number_of_captures = max([sequence.length for sequence in moves])
            moves = [sequence for sequence in moves if sequence.length == max_number_of_captures]
        return moves

    def get_potential_noncapture_sequences_for_man(self, piece: Piece) -> list[SequenceOfMoves]:
        list_of_sequences = []
        left_col = piece.col - 1
        right_col = piece.col + 1
        if piece.player == Player.PLAYER_TOP:
            target_row = piece.row + 1
        else:  # Player.PLAYER_BOTTOM:
            target_row = piece.row - 1
        if not self._is_out_of_bound(target_row, left_col):
            if self.board[target_row][left_col] == 0:
                list_of_sequences.append(SequenceOfMoves(piece, [Move(piece.row, piece.col, target_row, left_col)]))
        if not self._is_out_of_bound(target_row, right_col):
            if self.board[target_row][right_col] == 0:
                list_of_sequences.append(SequenceOfMoves(piece, [Move(piece.row, piece.col, target_row, right_col)]))
        return list_of_sequences


    def get_potential_capture_sequences_for_man(self, piece, row, col, captured_pieces=[]):
        list_of_possible_sequences = []
        for horizontal_step in (-1, 1): # for every diagonal
            for vertical_step in (-1, 1):
                row_after_capture = row+2*vertical_step
                col_after_capture = col+2*horizontal_step
                # if there is a space for capture in that direction (2 fields)
                if not self._is_out_of_bound(row_after_capture, col_after_capture):
                    field_content = self.get_piece(row+vertical_step, col+horizontal_step)
                    # if neighbouring field is an enemy piece and was not already captured in current sequence
                    if isinstance(field_content, Piece):
                        if field_content.is_rival_piece(piece) and field_content not in captured_pieces:
                            field_behind_rival_piece_content = self.get_piece(row_after_capture, col_after_capture)
                            # if field behind rival piece is empty or would be empty after moving current piece
                            if field_behind_rival_piece_content == 0 or field_behind_rival_piece_content == piece:
                                current_move = Move(row, col, row_after_capture, col_after_capture, field_content)
                                # modify copy of list of captured pieces as original is needed for next loop iteration
                                updated_captured_pieces = captured_pieces + [field_content]
                                # pass list of captured pieces in current sequence including one made in this iteration
                                list_of_sequence_continuation = self.get_potential_capture_sequences_for_man\
                                    (piece, row_after_capture, col_after_capture, updated_captured_pieces)
                                if not list_of_sequence_continuation:
                                    list_of_possible_sequences.append(SequenceOfMoves(piece, [current_move]))
                                else:
                                    for seq in list_of_sequence_continuation:
                                        seq.add_previous_move(current_move)
                                        list_of_possible_sequences.append(seq)
        return list_of_possible_sequences

    def _find_piece_to_capture_on_diagonal(self, row, col, vertical_step, horizontal_step, piece: Piece) -> tuple[bool, Piece] | tuple[bool, None]:
        # check if there is rival piece on diagonal and there is at least 1 free field behind piece,
        # it means that piece capturing is possible for queen
        is_piece_on_way = False
        row_examined = row + vertical_step
        col_examined = col + horizontal_step
        while 0 < row_examined < ROWS - 1 and 0 < col_examined < COLUMNS - 1 and not is_piece_on_way:
            field_content = self.get_piece(row_examined, col_examined)
            if isinstance(field_content, Piece) and field_content != piece:  # piece is not an obstacle for itself
                is_piece_on_way = True
            row_examined += vertical_step
            col_examined += horizontal_step
        if is_piece_on_way:
            if field_content.is_rival_piece(piece):
                field_behind_enemy_piece = self.get_piece(field_content.row + vertical_step, field_content.col + horizontal_step)
                if field_behind_enemy_piece == 0 or field_behind_enemy_piece == piece:
                    return True, field_content
        return False, None

    def get_potential_capture_sequences_for_queen(self, piece: Piece, row, col, captured_pieces=[]):
        possible_sequences = []
        for vertical_step in (-1, 1):
            for horizontal_step in (-1, 1): # for every diagonal
                is_capture_possible, enemy_piece = self._find_piece_to_capture_on_diagonal(row, col, vertical_step, horizontal_step, piece)
                if is_capture_possible and enemy_piece not in captured_pieces:
                    row_examined = enemy_piece.row + vertical_step
                    col_examined = enemy_piece.col + horizontal_step
                    while not self._is_out_of_bound(row_examined, col_examined):
                        field_content = self.get_piece(row_examined, col_examined)
                        if field_content != 0:
                            break
                        current_move = Move(row, col, row_examined, col_examined, enemy_piece)
                        updated_captured_pieces = captured_pieces + [enemy_piece]
                        sequence_continuation = self.get_potential_capture_sequences_for_queen(piece, row_examined, col_examined, updated_captured_pieces)
                        if sequence_continuation:
                            for seq in sequence_continuation:
                                seq.add_previous_move(current_move)
                                possible_sequences.append(seq)
                        else:
                            possible_sequences.append(SequenceOfMoves(piece, [current_move]))
                        row_examined += vertical_step
                        col_examined += horizontal_step
        return possible_sequences

    def get_potential_noncapture_sequences_for_queen(self, piece: Piece):
        possible_sequences = []
        for vertical_step in (-1, 1):
            for horizontal_step in (-1, 1):  # for every diagonal
                examined_row = piece.row + vertical_step
                examined_col = piece.col + horizontal_step
                while not self._is_out_of_bound(examined_row, examined_col):
                    field_content = self.get_piece(examined_row, examined_col)
                    if field_content != 0:
                        break
                    current_move = Move(piece.row, piece.col, examined_row, examined_col)
                    possible_sequences.append(SequenceOfMoves(piece, [current_move]))
                    examined_row += vertical_step
                    examined_col += horizontal_step
        return possible_sequences

    def remove_piece(self, piece: Piece):
        self.board[piece.row][piece.col] = 0

