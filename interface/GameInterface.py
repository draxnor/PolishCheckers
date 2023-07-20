import pygame
from checkers.Piece import Piece
from checkers.Move import Move
from checkers.Game import Game
from graphics.graphics_constants import SQUARE_HEIGHT, SQUARE_WIDTH
from graphics.GameGraphics import GameGraphics
from minimax.Minimax import Minimax
from checkers.Player import Player
from enum import Enum, auto


class SelectionStatus(Enum):
    MOVE_EXECUTED_SEQUENCE_UNFINISHED = auto()
    MOVE_EXECUTED_SEQUENCE_FINISHED = auto()
    NEW_PIECE_SELECTED = auto()
    SELECTION_INVALID = auto()
    GAMEOVER = auto()


class GameInterface:
    def __init__(self, game: Game, window: pygame.Surface):
        self.game = game
        self.graphics = GameGraphics(window)
        self.selected = None
        self.is_sequence_ongoing = False
        self.ai_max_depth = 4
        self.ai_bot = Minimax(self.ai_max_depth)

    def reset(self):
        self.game.reset()
        self.game.initialize_from_custom_state() #todo
        self.selected = None
        self.is_sequence_ongoing = False

    def ai_move(self, using_pruning: bool = True):
        is_maximizing_player = self.game.turn == Player.PLAYER_TOP

        if using_pruning:
            best_value, best_sequence = self.ai_bot.run_minimax_with_branch_pruning(self.game, depth=self.ai_max_depth, is_maximizing_player=is_maximizing_player)
        else:
            best_value, best_sequence = self.ai_bot.run_minimax(self.game, depth=self.ai_max_depth,is_maximizing_player=is_maximizing_player)
        self.game.execute_sequence_and_set_new_turn(best_sequence)
        print(f'Best found evaluation: {best_value}. Pruning: {using_pruning}')


    @staticmethod
    def get_board_coordinates_from_mouse_pos(pos: tuple[int, int]) -> tuple[int, int]:
        x, y = pos
        row = y // SQUARE_HEIGHT
        col = x // SQUARE_WIDTH
        return row, col

    def select(self, mouse_pos: tuple[int, int]) -> SelectionStatus:
        # If piece marked as selected and move possible, process move.
        # If sequence is already ongoing, then invalid selections are ignored. You have to finish one of valid sequences
        # If move impossible or nothing was selected before, select new piece if possible.
        if self.game.is_game_over():
            return SelectionStatus.GAMEOVER

        row, col = self.get_board_coordinates_from_mouse_pos(mouse_pos)
        if isinstance(self.selected, Piece):
            move_to_make = Move(self.selected, self.selected.row, self.selected.col,  row, col)
            is_move_done, can_sequence_be_continued = self.game.execute_single_move(move_to_make)
            if is_move_done:
                if can_sequence_be_continued:
                    return SelectionStatus.MOVE_EXECUTED_SEQUENCE_UNFINISHED
                self.selected = None
                self.game.end_turn()
                return SelectionStatus.MOVE_EXECUTED_SEQUENCE_FINISHED
                # while not self.game.is_game_over():
                #     self.update_display()
                #     self.ai_move(using_pruning=False)
                #     time.sleep(0.5)
                #     if self.game.is_game_over():
                #         break
                #     self.update_display()
                #     self.ai_move(using_pruning=True)
                #     time.sleep(0.5)
                # print(self.game.valid_moves[0])

        new_selection = self.game.board.get_piece(row, col)
        if isinstance(new_selection, Piece) and new_selection.player == self.game.turn:
            self.selected = new_selection
            return SelectionStatus.NEW_PIECE_SELECTED

        self.selected = None
        return SelectionStatus.SELECTION_INVALID

    def update_display(self) -> None:
        self.graphics.draw_background()
        if self.selected is not None:
            self.graphics.draw_valid_moves_of_selected_piece(self.game, self.selected)
        self.graphics.draw_pieces(self.game.board)
        if self.game.is_game_over():
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
