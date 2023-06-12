import pygame
from .Board import Board
from .Player import Player
from .Piece import Piece
from .Move import Move
from .GameState import GameState


class Game:
    def __init__(self, window):
        self._init()
        self.window = window

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = Player.PLAYER_TOP
        self.valid_moves = []
        self.is_sequence_ongoing = False
        self.set_new_turn()
        self.state = GameState.ONGOING
        self.board_state_history = []

    def update(self):
        # print(self.board.get_piece_count())
        self.board.draw_background(self.window)
        self.highlight_valid_moves_of_selected_piece()
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
            if move_done:  # (and not self.is_sequence_ongoing)
                self.selected = None
                self.change_turn()
                self.set_new_turn()
                self.check_for_game_ending()
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
        self.board.perform_pieces_promotions()
        self.calculate_valid_moves()

    def check_for_draw(self):
        pass
        # TODO

    def check_gameover_with_loss(self):
        return not self.valid_moves

    def update_game_state(self):
        if self.check_gameover_with_loss():
            if self.turn == Player.PLAYER_TOP:
                self.state = GameState.PLAYER_BOTTOM_WON
            else:
                self.state = GameState.PLAYER_TOP_WON
            return
        if self.check_for_draw():
            self.state = GameState.DRAW
            return

    def calculate_valid_moves(self):
        self.valid_moves = self.board.get_valid_moves(self.turn)

    def _move(self, destination_row, destination_col):
        # try moving self.selected to destination
        # create list of sequences that contains
        move_to_make = Move(self.selected.row, self.selected.col, destination_row, destination_col)
        is_move_possible = False

        sequences_that_contained_move = []
        for seq in self.valid_moves:
            if move_to_make.is_same_origin_and_destination(seq.first_move):
                is_move_possible = True
                move_to_make = seq.pop()
                if not seq.is_empty():
                    sequences_that_contained_move.append(seq)
        if is_move_possible:
            self.board.perform_move(self.selected, move_to_make)
            if sequences_that_contained_move:
                self.is_sequence_ongoing = True
            else:
                self.is_sequence_ongoing = False
            self.valid_moves = sequences_that_contained_move
            return True
        else:
            return False

    def highlight_valid_moves(self, list_of_sequences):
        for sequence in list_of_sequences:
            sequence.highlight_sequence(self.window)

    def change_turn(self):
        if self.turn == Player.PLAYER_TOP:
            self.turn = Player.PLAYER_BOTTOM
        else:
            self.turn = Player.PLAYER_TOP


