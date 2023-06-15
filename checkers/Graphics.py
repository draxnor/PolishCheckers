import pygame
from .Board import Board
from .Piece import Piece
from .SequenceOfMoves import SequenceOfMoves
from .Move import Move
from .game_constants import ROWS, COLUMNS
from .graphics_constants import PIECE_RADIUS, CROWN_COLOR, SQUARE_HEIGHT, SQUARE_WIDTH, HIGHLIGHT_COLOR, \
                                MOVE_DOT_RADIUS, CHECKERBOARD_BACKGROUND_COLOR, CHECKERBOARD_SQUARES_COLOR
from .Game import Game


class Graphics:
    def __init__(self, window: pygame.Surface) -> None:
        self.window = window

    def draw_valid_moves_of_selected_piece(self, game: Game, selected_piece: Piece) -> None:
        piece_valid_sequences = game.get_valid_sequences_of_a_piece(selected_piece)
        for sequence in piece_valid_sequences:
            self.draw_sequence(sequence)
            self.draw_first_move_in_sequence_highlight(sequence)

    def draw_piece(self, piece: Piece) -> None:
        pygame.draw.circle(self.window, piece.color, piece.position_on_display, PIECE_RADIUS)
        if piece.is_queen:
            pygame.draw.circle(self.window, CROWN_COLOR, piece.position_on_display, PIECE_RADIUS // 2)

    def draw_sequence(self, sequence: SequenceOfMoves) -> None:
        for move in sequence.sequence:
            self.draw_move_dot_hint(move)

    def draw_first_move_in_sequence_highlight(self, sequence: SequenceOfMoves, position: int = 0) -> None:
        self.draw_move_highlight(sequence.sequence[-position-1])

    def draw_move_dot_hint(self, move: Move) -> None:
        destination_row, destination_col = move.destination
        destination_square_center = (destination_col * SQUARE_WIDTH + SQUARE_WIDTH//2,
                                     destination_row * SQUARE_HEIGHT + SQUARE_HEIGHT//2)
        pygame.draw.circle(self.window, HIGHLIGHT_COLOR, destination_square_center, MOVE_DOT_RADIUS)

    def draw_move_highlight(self, move: Move) -> None:
        destination_row, destination_col = move.destination
        square = pygame.Rect((destination_col * SQUARE_WIDTH, destination_row*SQUARE_HEIGHT),
                             (SQUARE_WIDTH, SQUARE_HEIGHT))
        pygame.draw.rect(self.window, HIGHLIGHT_COLOR, square)

    def draw_square(self, row: int, col: int, color: tuple[int, int, int]) -> None:
        pygame.draw.rect(self.window, color, pygame.Rect((col*SQUARE_WIDTH, row*SQUARE_HEIGHT),
                                                         (SQUARE_WIDTH, SQUARE_HEIGHT)))

    def draw_background(self) -> None:
        self.window.fill(CHECKERBOARD_BACKGROUND_COLOR)
        for row in range(ROWS):
            for col in range(COLUMNS):
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                    self.draw_square(row, col, CHECKERBOARD_SQUARES_COLOR)

    def draw_empty_board(self) -> None:
        self.draw_background()
        self.draw_pieces()

    def draw_pieces(self, board: Board) -> None:
        for row in range(ROWS):
            for col in range(COLUMNS):
                field_content = board.get_piece(row, col)
                if isinstance(field_content, Piece):
                    self.draw_piece(field_content)

    def draw_multiple_sequences(self, valid_sequences: list[SequenceOfMoves]) -> None:
        # Only for custom visualisation and debugging
        for sequence in valid_sequences:
            self.draw_sequence(sequence)

