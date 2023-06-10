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
        self.is_sequence_ongoing = False

    def update(self):
        self.board.draw_background(self.window)
        self.highlight_valid_moves_of_selected_piece()
        print(self.selected)
        self.board.draw_pieces(self.window)
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, row, col):
        # If piece marked as selected and move possible, process move.
        # If sequence is already ongoing, then invalid selections are ignored. You have to finish one of valid sequences
        # If move impossible or nothing was selected before, select new piece if possible.
        if isinstance(self.selected, Piece):
            move_done = self._move(row, col)
            if self.is_sequence_ongoing:
                return
            if move_done:
                self.selected = None
                self.set_new_turn()
                return
        new_selection = self.board.get_piece(row, col)
        if isinstance(new_selection, Piece) and new_selection.player == self.turn:
            self.selected = new_selection
            return
        self.selected = None

    def get_valid_moves_of_selected_piece(self):
        return [sequence for sequence in self.valid_moves if sequence.get_moving_piece() == self.selected]

    def highlight_valid_moves_of_selected_piece(self):
        piece_valid_sequences = self.get_valid_moves_of_selected_piece()
        for sequence in piece_valid_sequences:
            sequence.draw_sequence(self.window)
            sequence.draw_move_in_sequence_as_closest(self.window, 0)

    def set_new_turn(self):
        self.change_turn()
        self.calculate_valid_moves()
        self.check_for_game_ending()

    def check_for_game_ending(self):
        #TODO
        # checking the winner
        # checking conditions for draw
        is_game_end = False
        if not self.valid_moves:
            is_game_end = True
        return is_game_end

    def calculate_valid_moves(self):
        self.valid_moves = self.board.get_valid_moves(self.turn)

    def _move(self, row, col):
        #TODO
        # For chosen piece
        # move = Move(self.selected.row, self.selected.col, )
        # self.board.move(move)
        return False

    def highlight_valid_moves(self, list_of_sequences):
        for sequence in list_of_sequences:
            sequence.highlight_sequence(self.window)

    def change_turn(self):
        if self.turn == Player.PLAYER_TOP:
            self.turn = Player.PLAYER_BOTTOM
        else:
            self.turn = Player.PLAYER_TOP


