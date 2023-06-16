import pygame
from .Piece import Piece
from .Move import Move
from .Game import Game
from .graphics_constants import SQUARE_HEIGHT, SQUARE_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH
from .Graphics import Graphics
from .GameState import GameState
from minimax.Minimax import Minimax
import time


class GameInterface:
    def __init__(self, game: Game, window: pygame.Surface):
        self.game = game
        self.graphics = Graphics(window)
        self.selected = None
        self.is_sequence_ongoing = False
        self.ai_max_depth = 5
        self.ai_bot = Minimax()

    def reset(self):
        self.game.reset()
        self.game.initialize_from_custom_state()
        self.selected = None
        self.is_sequence_ongoing = False

    def ai_move(self):
        best_value, best_sequence = self.ai_bot.run_minimax(self.game, depth=self.ai_max_depth)
        self.game.execute_sequence_and_set_new_turn(best_sequence)

    @staticmethod
    def get_board_coordinates_from_mouse_pos(pos: tuple[int, int]) -> tuple[int, int]:
        x, y = pos
        row = y // SQUARE_HEIGHT
        col = x // SQUARE_WIDTH
        return row, col

    def select(self, mouse_pos: tuple[int, int]) -> None:
        # If piece marked as selected and move possible, process move.
        # If sequence is already ongoing, then invalid selections are ignored. You have to finish one of valid sequences
        # If move impossible or nothing was selected before, select new piece if possible.
        row, col = self.get_board_coordinates_from_mouse_pos(mouse_pos)
        if isinstance(self.selected, Piece):
            move_to_make = Move(self.selected, self.selected.row, self.selected.col,  row, col)
            is_move_done, can_sequence_be_continued = self.game.execute_single_move(move_to_make)
            if can_sequence_be_continued:
                return
            if is_move_done:  # (and not can_sequence_be_continued)
                self.selected = None
                self.game.end_current_turn()
                self.game.change_turn()
                self.game.set_new_turn()
                # print(self.game.valid_moves[0])
                self.ai_move()
                return
        new_selection = self.game.board.get_piece(row, col)
        if isinstance(new_selection, Piece) and new_selection.player == self.game.turn:
            self.selected = new_selection
            return
        self.selected = None

    def update_display(self) -> None:
        self.graphics.draw_background()
        if self.selected is not None:
            self.graphics.draw_valid_moves_of_selected_piece(self.game, self.selected)
        self.graphics.draw_pieces(self.game.board)
        if self.game.state != GameState.ONGOING:
            self.graphics.draw_game_over_message(self.game)
        pygame.display.update()

    def print_game_state(self):
        message = '\n'.join([ '______________________________',
                  f'TOP MAN: {self.game.board.player_top_men_count}',
                  f'TOP QUEEN: {self.game.board.player_top_kings_count}',
                  f'BOT MAN: {self.game.board.player_bottom_men_count}',
                  f'TOP QUEEN: {self.game.board.player_bottom_kings_count}',
                  f'NORMAL MOVES: {self.game.non_capture_moves_count}',
                  f'QUEEN MOVES: {self.game.non_capture_queens_moves_count}',
                  f'STATE: {self.game.state}'])
        print(message)
