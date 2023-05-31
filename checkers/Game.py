import pygame
from .Board import Board
from .Player import Player
from .Piece import Piece


class Game:
    def __init__(self, window):
        self.selected = None
        self.board = Board()
        self.turn = Player.PLAYER_TOP
        self.valid_moves = []
        self.window = window

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = Player.PLAYER_TOP
        self.valid_moves = {}

    def update(self):
        self.board.draw_board(self.window)
        self.highlight_possible_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, row, col):
        # If you click on board and something was already selected -> move selected piece to destination if possible
        # If you click on board and nothing was selected beforehand -> highlight possible moves for a piece,
        #   but only if you selected piece that belong to you
        if self.selected is not None:
            if isinstance(self.selected, Piece):
                success = False # self._move(row, col) #TODO
                if not success:
                    self.selected = None
            self.valid_moves = []

        if self.selected is None:
            piece = self.board.get_piece(row, col)
            if isinstance(piece, Piece) and piece.player == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves_of_piece(piece)


    def _move(self, row, col):
        #TODO
        return False

    def highlight_possible_moves(self, list_of_sequences):
        if list_of_sequences:
            for sequence in list_of_sequences:
                for move in sequence:
                    row, col = move.destination
                    self.board.highlight_square(self.window, row, col)

    def change_turn(self):
        if self.turn == Player.PLAYER_TOP:
            self.turn = Player.PLAYER_BOTTOM
        else:
            self.turn = Player.PLAYER_TOP
