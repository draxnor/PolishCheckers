import pygame
from .Board import Board
from .Player import Player
from .Piece import Piece

class Game:
    def __init__(self, window):
        self.selected = None
        self.board = Board()
        self.turn = Player.PLAYER_TOP
        self.valid_moves = {}
        self.window = window

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = Player.PLAYER_TOP
        self.valid_moves = {}

    def update(self):
        self.board.draw_board(self.window)
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected is not None:
            if isinstance(self.selected, Piece):
                success = self._move(row, col)
                if not success:
                    self.selected = None
                    #self.selected = self.select(row, col)
        piece = self.board.get_piece(row, col)
        if isinstance(piece, Piece) and piece.player == self.turn:
            self.selected = piece
            # self.board.highlight_as_selected(piece)
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False
        #if you try to select piece -> select and highlight possible moves
        #if you try to select empty square and nothing was selected beforehand -> select nothing

    def _move(self, row, col):
        pass

    def change_turn(self):
        if self.turn == Player.PLAYER_TOP:
            self.turn = Player.PLAYER_BOTTOM
        else:
            self.turn = Player.PLAYER_TOP
    #     if self.selected