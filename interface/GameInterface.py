import pygame
from checkers.Piece import Piece
from checkers.Move import Move
from checkers.Game import Game
from graphics.graphics_constants import SQUARE_HEIGHT, SQUARE_WIDTH, \
    GAME_WINDOW_HORIZONTAL_OFFSET, GAME_WINDOW_VERTICAL_OFFSET
from graphics.GameGraphics import GameGraphics
from minimax.Minimax import Minimax
from checkers.Player import Player
from enum import Enum, auto
from interface.GameplayOptions import GameplayOptions, PlayerType, PlayerSide
import random


class SelectionStatus(Enum):
    MOVE_EXECUTED_SEQUENCE_UNFINISHED = auto()
    MOVE_EXECUTED_SEQUENCE_FINISHED = auto()
    NEW_PIECE_SELECTED = auto()
    SELECTION_INVALID = auto()
    GAMEOVER = auto()
    NOT_A_HUMAN_TURN = auto()


class GameInterface:
    def __init__(self, window: pygame.Surface, gameplay_options: GameplayOptions):
        self.gameplay_options = gameplay_options
        self.game = self._create_game(gameplay_options)
        self.graphics = GameGraphics(window)
        self.selected = None
        self.is_sequence_ongoing = False
        if gameplay_options.top_player_type == PlayerType.Human:
            self.ai_top = None
        elif gameplay_options.top_player_type == PlayerType.AI:
            self.ai_top = Minimax(gameplay_options.top_ai_depth)
        if gameplay_options.bottom_player_type == PlayerType.Human:
            self.ai_bottom = None
        elif gameplay_options.bottom_player_type == PlayerType.AI:
            self.ai_bottom = Minimax(gameplay_options.bottom_ai_depth)

    def _create_game(self, gameplay_options: GameplayOptions):
        if gameplay_options.starting_side == PlayerSide.TOP:
            starting_player = Player.PLAYER_TOP
        else:
            starting_player = Player.PLAYER_BOTTOM
        return Game(starting_player)

    def reset(self):
        self.game.reset()
        self.game.initialize_from_custom_state()
        self.selected = None
        self.is_sequence_ongoing = False

    def perform_ai_move(self, using_pruning: bool = True):
        if self.game.is_game_over():
            return
        if self.is_human_turn():
            return
        is_maximizing_player = self.game.turn == Player.PLAYER_TOP
        if self.game.turn == Player.PLAYER_TOP:
            current_ai = self.ai_top
        else:
            current_ai = self.ai_bottom
        if current_ai.max_depth == 0:
            best_value = -1
            rand_int = random.randrange(0, len(self.game.valid_moves))
            best_sequence = self.game.valid_moves[rand_int]
        else:
            if using_pruning:
                best_value, best_sequence = current_ai.run_minimax_with_branch_pruning(self.game,
                                                                                       is_maximizing_player=is_maximizing_player)
            else:
                best_value, best_sequence = current_ai.run_minimax(self.game, is_maximizing_player=is_maximizing_player)
        self.game.execute_sequence_and_set_new_turn(best_sequence)
        # print(f'Best found evaluation: {best_value}. Maximazing:', 'Yes' if is_maximizing_player else 'No')

    def is_human_turn(self):
        if (self.game.turn == Player.PLAYER_TOP and self.gameplay_options.top_player_type == PlayerType.Human) or \
             (self.game.turn == Player.PLAYER_BOTTOM and self.gameplay_options.bottom_player_type == PlayerType.Human):
            return True
        return False

    def select(self, mouse_pos: tuple[int, int]) -> SelectionStatus:
        # If piece marked as selected and move possible, process move.
        # If sequence is already ongoing, then invalid selections are ignored. You have to finish one of valid sequences
        # If move impossible or nothing was selected before, select new piece if possible.
        if self.game.is_game_over():
            return SelectionStatus.GAMEOVER

        if not self.is_human_turn():
            return SelectionStatus.NOT_A_HUMAN_TURN

        row, col = self.get_board_coordinates_from_mouse_pos(mouse_pos)
        if isinstance(self.selected, Piece):
            move_to_make = Move(self.selected, self.selected.row, self.selected.col, row, col)
            is_move_done, can_sequence_be_continued = self.game.execute_single_move(move_to_make)
            if is_move_done:
                if can_sequence_be_continued:
                    return SelectionStatus.MOVE_EXECUTED_SEQUENCE_UNFINISHED
                self.selected = None
                self.game.end_turn()
                return SelectionStatus.MOVE_EXECUTED_SEQUENCE_FINISHED

        new_selection = self.game.board.get_piece(row, col)
        if isinstance(new_selection, Piece) and new_selection.player == self.game.turn:
            self.selected = new_selection
            return SelectionStatus.NEW_PIECE_SELECTED

        self.selected = None
        return SelectionStatus.SELECTION_INVALID

    def update_display(self) -> None:
        self.graphics.clear_main_window()
        self.graphics.draw_background()
        if self.selected is not None:
            self.graphics.draw_valid_moves_of_selected_piece(self.game, self.selected)
        self.graphics.draw_pieces(self.game.board)
        if self.game.is_game_over():
            self.graphics.draw_gameover_message(self.game)
        self.graphics.draw_turn_information(self.game.turn, self.is_human_turn())
        self.graphics.draw_game_window_on_main_window()
        pygame.display.update()

    def print_game_state(self):
        message = '\n'.join(['______________________________',
                             f'TOP MAN: {self.game.board.player_top_men_count}',
                             f'TOP QUEEN: {self.game.board.player_top_kings_count}',
                             f'BOT MAN: {self.game.board.player_bottom_men_count}',
                             f'TOP QUEEN: {self.game.board.player_bottom_kings_count}',
                             f'NORMAL MOVES: {self.game.non_capture_moves_count}',
                             f'QUEEN MOVES: {self.game.non_capture_queens_moves_count}',
                             f'STATE: {self.game.state}'])
        print(message)

    @staticmethod
    def get_board_coordinates_from_mouse_pos(pos: tuple[int, int]) -> tuple[int, int]:
        x_main_screen, y_main_screen = pos
        x, y = x_main_screen - GAME_WINDOW_HORIZONTAL_OFFSET, y_main_screen - GAME_WINDOW_VERTICAL_OFFSET
        row = y // SQUARE_HEIGHT
        col = x // SQUARE_WIDTH
        return row, col