from __future__ import annotations
import pygame
from .Piece import Piece
from .constants import HIGHLIGHT_COLOR, SQUARE_HEIGHT, SQUARE_WIDTH, MOVE_DOT_RADIUS


class Move:
    def __init__(self, start_row: int, start_col: int, target_row: int, target_col: int,
                 captured_piece: Piece = None) -> None:
        self.origin_row = start_row
        self.origin_col = start_col
        self.destination_row = target_row
        self.destination_col = target_col
        self.captured_piece = captured_piece

    def __repr__(self) -> str:
        repr_str = 'From:' + str((self.origin_row, self.origin_col)) + \
                   ' To:' + str((self.destination_row, self.destination_col)) + \
                   ', capturing: ' + str(self.captured_piece)
        return repr_str

    def __eq__(self, other: Move) -> bool:
        return self.is_same_origin_and_destination(other) and self.captured_piece == other.captured_piece

    def is_same_origin_and_destination(self, other: Move) -> bool:
        return self.origin_row == other.origin_row and self.origin_col == other.origin_col and \
               self.destination_row == other.destination_row and self.destination_col == other.destination_col

    @property
    def destination(self) -> tuple[int, int]:
        return self.destination_row, self.destination_col

    @property
    def origin(self) -> tuple[int, int]:
        return self.origin_row, self.origin_col

    def does_contain_capture(self) -> bool:
        return self.captured_piece is not None

    def draw_move_destination_as_distant_move(self, window: pygame.Surface) -> None:
        destination_square_center =  (self.destination_col * SQUARE_WIDTH + SQUARE_WIDTH//2,
                                      self.destination_row * SQUARE_HEIGHT + SQUARE_HEIGHT//2)
        pygame.draw.circle(window, HIGHLIGHT_COLOR, destination_square_center, MOVE_DOT_RADIUS)

    def draw_move_destination_as_closest_move(self, window: pygame.Surface) -> None:
        square = pygame.Rect((self.destination_col * SQUARE_WIDTH, self.destination_row*SQUARE_HEIGHT),
                             (SQUARE_WIDTH, SQUARE_HEIGHT))
        pygame.draw.rect(window, HIGHLIGHT_COLOR, square)

