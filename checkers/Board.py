import pygame
from .constants import *
from .Piece import Piece
from .Player import Player

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
                if (row%2 == 0 and col%2 == 0) or (row%2 != 0 and col%2 != 0):
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
        moves = {}
        #look for captures first
        #if capture possible, leave only those with the highest possible capture count
        #if captures impossible, leave only normal moves
        if piece.is_king == True:
            moves.update(self.get_possible_captures_for_king(piece))
            if not moves:
                moves.update(self.get_possible_noncapture_moves_for_king(piece))
        else:
            moves.update(self.get_possible_captures_for_man(piece))
            if not moves:
                moves.update(self.get_possible_noncapture_moves_for_man(piece))
        return moves

    def get_possible_captures_for_king(self, piece):
        pass

    def get_possible_noncapture_moves_for_man(self, piece):
        list_of_moves = []
        left_col = piece.col - 1
        right_col = piece.col + 1
        if piece.player == Player.PLAYER_TOP:
            target_row = piece.row + 1
        if piece.player == Player.PLAYER_BOTTOM:
            target_row = piece.row - 1
        if target_row >= 0 and target_row < ROWS:
            if left_col >= 0:
                if self.board[target_row][left_col] == 0:
                    list_of_moves.append((target_row, left_col))
                #check if empty field
            if right_col < ROWS:
                if self.board[target_row][right_col] == 0:
                    list_of_moves.append((target_row, right_col))
        moves = {0: list_of_moves}
