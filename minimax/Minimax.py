from checkers.Game import Game
from checkers.GameState import GameState


class Minimax():
    def __init__(self, max_depth: int=1, queen_value: float=3) -> None:
        self.max_depth = max_depth
        self.queen_value = queen_value

    def evaluate_position(self, game_state: Game):
        if game_state.is_game_over():
            if game_state.state == GameState.DRAW:
                return 0
            if game_state.state == GameState.PLAYER_TOP_WON:
                return float('inf')
            if game_state.state == GameState.PLAYER_BOTTOM_WON:
                return float('-inf')
        top_man, top_queens, bot_man, bot_queens = game_state.board.piece_count_detailed
        return top_man - bot_man + (top_queens - bot_queens)*self.queen_value

    def run_minimax(self, game_state: Game, depth: int = None,
                    alpha: float = float('-inf'), beta: float = float('inf'),
                    is_maximizing_player: bool = False):

        if depth is None:
            depth = self.max_depth

        if depth == 0 or game_state.is_game_over():
            return self.evaluate_position(game_state), None

        best_sequence = game_state.valid_moves[0]
        if is_maximizing_player:
            max_eval = float('-inf')
            for sequence in game_state.valid_moves:
                child = game_state.deepcopy()
                child.execute_sequence_and_set_new_turn(sequence)
                value = self.run_minimax(child, depth-1, alpha, beta, False)[0]
                if max_eval < value:
                    max_eval = value
                    best_sequence = sequence
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return max_eval, best_sequence
        else:
            min_eval = float('inf')
            for sequence in game_state.valid_moves:
                child = game_state.deepcopy()
                child.execute_sequence_and_set_new_turn(sequence)
                value = self.run_minimax(child, depth-1, alpha, beta, True)[0]
                if value < min_eval:
                    min_eval = value
                    best_sequence = sequence
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return min_eval, best_sequence
