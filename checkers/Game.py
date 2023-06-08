import pygame
from .Board import Board
from .Player import Player
from .Piece import Piece
from .Move import Move

class Game:
    def __init__(self, window):
        self._init()
        self.window = window

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = Player.PLAYER_TOP
        self.valid_moves = {}

    def update(self):
        self.board.draw_background(self.window)
        self.highlight_possible_moves(self.valid_moves)
        self.board.draw_pieces(self.window)
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, row, col):
        # If you click on board and something was already selected -> move selected piece to destination if possible
        # If you click on board and nothing was selected beforehand -> highlight possible moves for a piece,
        #   but only if you selected piece that belong to you
        if self.selected is not None:
            if isinstance(self.selected, Piece):
                success = self._move(row, col) #TODO
                self.selected = None
                if not success:
                    self.selected = None
            self.valid_moves = []

        if self.selected is None:
            piece = self.board.get_piece(row, col)
            if isinstance(piece, Piece) and piece.player == self.turn:
                print(f'Piece belongs to {piece.player} when it is turn of {self.turn}')
                self.selected = piece
                self.valid_moves = self.board.get_potential_sequences_for_piece(piece)


    def _move(self, row, col):
        #TODO
        # For chosen piece
        # move = Move(self.selected.row, self.selected.col, )
        # self.board.move(move)
        return True

    def highlight_possible_moves(self, list_of_sequences):
        if list_of_sequences:
            for seq in list_of_sequences:
                for move in seq.sequence:
                    row, col = move.destination
                    self.board.highlight_square(self.window, row, col)

    def change_turn(self):
        if self.turn == Player.PLAYER_TOP:
            self.turn = Player.PLAYER_BOTTOM
        else:
            self.turn = Player.PLAYER_TOP
