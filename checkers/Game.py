import pygame
from .Board import Board
from .Player import Player
from .Piece import Piece
from .Move import Move
from .SequenceOfMoves import SequenceOfMoves
from .GameState import GameState
from .constants import NONCAPTURE_QUEEN_MOVES_COUNT_LIMIT, BOARD_STATE_REPETITION_LIMIT, \
    MOVES_COUNT_FOR_1V3_ENDGAME, MOVES_COUNT_FOR_1V2_ENDGAME, MOVES_COUNT_FOR_1V1_ENDGAME


class Game:
    def __init__(self, window: pygame.Surface) -> None:
        self._init()
        self.window = window

    def _init(self) -> None:
        self.selected = None
        self.board = Board()
        self.turn = Player.PLAYER_TOP
        self.valid_moves = []
        self.is_sequence_ongoing = False
        self.state = GameState.ONGOING
        self.noncapture_queens_moves_count = 0
        self.move_count_to_draw = 0
        self.board_state_history = []
        self.save_board_state()
        self.set_new_turn()

    def update_display(self) -> None:
        print(self.state.name)
        self.board.draw_background(self.window)
        self.draw_valid_moves_of_selected_piece()
        self.board.draw_pieces(self.window)
        pygame.display.update()

    def reset(self) -> None:
        self._init()

    def select(self, mouse_pos: tuple[int, int]) -> None:
        # If piece marked as selected and move possible, process move.
        # If sequence is already ongoing, then invalid selections are ignored. You have to finish one of valid sequences
        # If move impossible or nothing was selected before, select new piece if possible.
        row, col = Board.get_coordinates_from_mouse_pos(mouse_pos)
        if isinstance(self.selected, Piece):
            is_move_done = self._execute_move(row, col)
            if self.is_sequence_ongoing:
                return
            if is_move_done:  # (and not self.is_sequence_ongoing)
                self.selected = None
                self.change_turn()
                self.set_new_turn()
                return
        new_selection = self.board.get_piece(row, col)
        if isinstance(new_selection, Piece) and new_selection.player == self.turn:
            self.selected = new_selection
            return
        self.selected = None

    def execute_sequence(self, sequence: SequenceOfMoves):
        pass #todo

    def save_board_state(self) -> None:
        self.board_state_history.append(self.board.deepcopy())

    def set_new_turn(self) -> None:
        self.board.perform_pieces_promotions()
        self.update_valid_moves()
        self.save_board_state()
        self.update_game_state()

    def _count_queen_moves_for_draw(self, last_made_move: Move) -> None:
        if self.selected.is_queen and not last_made_move.does_contain_capture():
            self.noncapture_queens_moves_count += 1
        else:
            self.noncapture_queens_moves_count = 0

    def _count_moves_for_endgame_draw(self, move_made: Move) -> None:
        if move_made.does_contain_capture():
            self.move_count_to_draw = 0
        else:
            self.move_count_to_draw += 1

    def _is_draw_by_queen_moves_count(self) -> bool:
        return self.noncapture_queens_moves_count >= NONCAPTURE_QUEEN_MOVES_COUNT_LIMIT

    def _is_draw_by_state_repetition(self) -> bool:
        repetition_count = 0
        for board_state in self.board_state_history[::-2]:
            if self.board.piece_count_total != board_state.piece_count_total:
                break
            if self.board == board_state:
                repetition_count += 1
                if repetition_count >= BOARD_STATE_REPETITION_LIMIT:
                    return True
        return False

    def _is_draw_by_1v1_queen_endgame(self) -> bool:
        return self.board.piece_count_detailed == (0, 1, 0, 1) and \
               self.noncapture_queens_moves_count >= MOVES_COUNT_FOR_1V1_ENDGAME

    def _is_draw_by_1v2_queen_endgame(self) -> bool:
        if self.board.piece_count_total == 3:
            if self.board.player_bottom_kings_count >= 1 and self.board.player_top_kings_count >= 1:
                if self.move_count_to_draw >= MOVES_COUNT_FOR_1V2_ENDGAME:
                    return True
        return False

    def _is_draw_by_1v3_queen_endgame(self) -> bool:
        if self.board.piece_count_total == 4:
            if self.board.player_bottom_kings_count >= 1 and self.board.player_top_kings_count >= 1:
                if (self.board.player_bottom_kings_count == 1 and self.board.player_bottom_men_count) or\
                    (self.board.player_top_kings_count == 1 and self.board.player_top_men_count):
                    if self.move_count_to_draw >= MOVES_COUNT_FOR_1V3_ENDGAME:
                        return True
        return False

    def _is_draw(self) -> bool:
        if self._is_draw_by_1v1_queen_endgame():  # players have 1 queen each
            return True
        if self._is_draw_by_1v2_queen_endgame():
            return True
        if self._is_draw_by_1v3_queen_endgame():
            return True
        if self._is_draw_by_state_repetition():
            return True
        if self._is_draw_by_queen_moves_count():
            return True
        return False

    def _is_game_over_with_loss(self) -> bool:
        return not self.valid_moves

    def update_game_state(self) -> None:
        if self._is_game_over_with_loss():
            if self.turn == Player.PLAYER_TOP:
                self.state = GameState.PLAYER_BOTTOM_WON
            else:
                self.state = GameState.PLAYER_TOP_WON
            return
        if self._is_draw():
            self.state = GameState.DRAW
            return

    def update_valid_moves(self) -> None:
        self.valid_moves = self.board.get_valid_moves(self.turn)

    def get_valid_sequences_of_selected_piece(self) -> list[SequenceOfMoves]:
        return [sequence for sequence in self.valid_moves if sequence.moving_piece == self.selected]

    def draw_valid_moves_of_selected_piece(self) -> None:
        piece_valid_sequences = self.get_valid_sequences_of_selected_piece()
        for sequence in piece_valid_sequences:
            sequence.draw_sequence(self.window)
            sequence.draw_move_in_sequence_as_next_move(self.window)

    def _execute_move(self, destination_row: int, destination_col: int) -> bool:
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
                self._count_queen_moves_for_draw(move_to_make)
                self._count_moves_for_endgame_draw(move_to_make)
            self.valid_moves = sequences_that_contained_move
            return True
        else:
            return False

    def change_turn(self) -> None:
        if self.turn == Player.PLAYER_TOP:
            self.turn = Player.PLAYER_BOTTOM
        else:
            self.turn = Player.PLAYER_TOP

    def _draw_given_sequences(self, valid_sequences: list[SequenceOfMoves]) -> None:
        # Only for custom visualisation and debugging
        for sequence in valid_sequences:
            sequence.draw_sequence(self.window)

