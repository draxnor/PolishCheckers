from .Board import Board
from .Player import Player
from .Piece import Piece
from .Move import Move
from .SequenceOfMoves import SequenceOfMoves
from .GameState import GameState
from .game_constants import NON_CAPTURE_QUEEN_MOVES_COUNT_LIMIT, BOARD_STATE_REPETITION_LIMIT, \
    MOVES_COUNT_FOR_1V3_ENDGAME, MOVES_COUNT_FOR_1V2_ENDGAME, MOVES_COUNT_FOR_1V1_ENDGAME


class Game:
    def __init__(self, player_starting_game: Player = Player.PLAYER_TOP) -> None:
        self._init(player_starting_game)

    def _init(self, player_starting_game: Player = Player.PLAYER_TOP) -> None:
        self.board = Board()
        self.turn = player_starting_game
        self.valid_moves = []
        self.current_turn_sequence = None
        self.previous_turn_sequence = None
        self.state = GameState.ONGOING
        self.non_capture_queens_moves_count = 0
        self.non_capture_moves_count = 0
        self.board_state_history = []
        self.save_board_state()
        self.set_new_turn()

    def deepcopy(self):
        cls = self.__class__
        new_game = cls.__new__(cls)
        new_game.__dict__.update(self.__dict__)
        new_game.board = self.board.deepcopy()
        new_game.turn = self.turn
        new_game.valid_moves = self.valid_moves.copy()
        new_game.previous_turn_sequence = self.previous_turn_sequence
        new_game.current_turn_sequence = self.current_turn_sequence
        new_game.state = self.state
        new_game.non_capture_queens_moves_count = self.non_capture_queens_moves_count
        new_game.non_capture_moves_count = self.non_capture_queens_moves_count
        new_game.board_state_history = self.board_state_history.copy()
        return new_game

    def reset(self) -> None:
        self._init()

    def save_board_state(self) -> None:
        self.board_state_history.append(self.board.deepcopy())

    def end_turn(self):
        self._set_current_sequence_as_previous()
        self.summarize_current_turn()
        self.change_turn()
        self.set_new_turn()

    def _set_current_sequence_as_previous(self):
        self.previous_turn_sequence = self.current_turn_sequence

    def summarize_current_turn(self):
        self._count_queen_moves_for_draw()
        self._count_moves_for_endgame_draw()
        self.board.perform_pieces_promotions()

    def set_new_turn(self) -> None:
        self._clear_current_turn_sequence()
        self.update_valid_moves()
        self.save_board_state()
        self.update_game_state()

    def _clear_current_turn_sequence(self):
        self.current_turn_sequence = None

    def _count_queen_moves_for_draw(self) -> None:
        assert(self.current_turn_sequence is not None, 'Cannot sum up turn where no move was done.')
        last_move_made = self.current_turn_sequence.last_move
        if last_move_made.moving_piece.is_queen and not last_move_made.does_contain_capture():
            self.non_capture_queens_moves_count += 1
        else:
            self.non_capture_queens_moves_count = 0

    def _count_moves_for_endgame_draw(self) -> None:
        assert(self.current_turn_sequence is not None, 'Cannot sum up turn where no move was done.')
        last_move_made = self.current_turn_sequence.last_move
        if last_move_made.does_contain_capture():
            self.non_capture_moves_count = 0
        else:
            self.non_capture_moves_count += 1

    def _is_draw_by_queen_moves_count(self) -> bool:
        return self.non_capture_queens_moves_count >= NON_CAPTURE_QUEEN_MOVES_COUNT_LIMIT

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
               self.non_capture_queens_moves_count >= MOVES_COUNT_FOR_1V1_ENDGAME

    def _is_draw_by_1v2_queen_endgame(self) -> bool:
        if self.board.piece_count_total == 3:
            if self.board.player_bottom_kings_count >= 1 and self.board.player_top_kings_count >= 1:
                if self.non_capture_moves_count >= MOVES_COUNT_FOR_1V2_ENDGAME:
                    return True
        return False

    def _is_draw_by_1v3_queen_endgame(self) -> bool:
        if self.board.piece_count_total == 4:
            if self.board.player_bottom_kings_count >= 1 and self.board.player_top_kings_count >= 1:
                if (self.board.player_bottom_kings_count == 1 and self.board.player_bottom_men_count == 0) or \
                        (self.board.player_top_kings_count == 1 and self.board.player_top_men_count == 0):
                    if self.non_capture_moves_count >= MOVES_COUNT_FOR_1V3_ENDGAME:
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

    def get_valid_sequences_of_a_piece(self, piece: Piece) -> list[SequenceOfMoves]:
        return [sequence for sequence in self.valid_moves if sequence.moving_piece == piece]

    def execute_single_move(self, move_to_make: Move) -> tuple[bool, bool]:
        can_move_be_done = False
        can_sequence_be_continued = False
        sequences_that_contained_move = []
        for seq in self.valid_moves:
            if move_to_make.is_same_origin_and_destination(seq.first_move):
                can_move_be_done = True
                move_to_make = seq.pop()  # get rest of the details about move
                if not seq.is_empty():
                    sequences_that_contained_move.append(seq)
        if can_move_be_done:
            self.board.perform_move(move_to_make)
            self.valid_moves = sequences_that_contained_move
            can_sequence_be_continued = True if self.valid_moves else False
            if self.current_turn_sequence is None:
                self.current_turn_sequence = SequenceOfMoves(move_to_make.moving_piece, [move_to_make])
            else:
                self.current_turn_sequence.add_next_move(move_to_make)
        return can_move_be_done, can_sequence_be_continued

    def change_turn(self) -> None:
        if self.turn == Player.PLAYER_TOP:
            self.turn = Player.PLAYER_BOTTOM
        else:
            self.turn = Player.PLAYER_TOP

    def execute_sequence(self, sequence_to_make: SequenceOfMoves) -> bool:
        #No conditions for executing sequence because of speed issues
        self.current_turn_sequence = sequence_to_make
        self.valid_moves.clear()
        for move in self.current_turn_sequence.sequence[::-1]:
            self.board.perform_move(move)
        return True

    def execute_sequence_and_set_new_turn(self, sequence_to_make: SequenceOfMoves) -> bool:
        success = self.execute_sequence(sequence_to_make)
        self.end_turn()
        return success

    def is_game_over(self):
        return self.state != GameState.ONGOING

    def _initialize_from_custom_state(self):
        for row in range(10):
            for col in range(10):
                self.board.board[row][col] = 0
        self.board.board[3][2] = Piece(3, 2, Player.PLAYER_TOP)
        self.board.board[3][2].promote()
        self.board.board[1][0] = Piece(1, 0, Player.PLAYER_BOTTOM)
        self.board.board[0][3] = Piece(0, 3, Player.PLAYER_BOTTOM)
        self.board.board[7][4] = Piece(7, 4, Player.PLAYER_BOTTOM)
        self.board.board[7][4].promote()
        self.board._recalculate_pieces_count()
        self.board_state_history = []
        self.save_board_state()
        self.set_new_turn()

