import pygame
from .constants import *
from .Piece import Piece
from .Player import Player

class Board():
    def __init__(self):
        self.board = [] #board state
        self.create_board()
        self.selected_piece = None
        self.player1_men_left = self.player2_men_left = 20
        self.player1_kings_left = self.player1_kings_left = 0

    def draw_board(self,window):
        self.draw_background(window)
        self.draw_pieces(window)

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
                if (row%2 + col%2) == 1:
                    if row < 4:
                        self.board[row].append(Piece(row,col,Player.PLAYER1))
                    elif row > 5:
                        self.board[row].append(Piece(row, col, Player.PLAYER2))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(-1)


