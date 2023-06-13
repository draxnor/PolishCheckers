import pygame
from .constants import SQUARE_HEIGHT, SQUARE_WIDTH, \
    PLAYER_TOP_COLOR, PLAYER_BOTTOM_COLOR, PIECE_RADIUS, CROWN_COLOR, \
    ROWS
from .Player import Player


class Piece:
    def __init__(self, row, col, player: Player):
        self.row = row
        self.col = col
        self.player = player
        self.is_queen = False

    def __eq__(self, other) -> bool:
        if not isinstance(other, Piece):
            return False
        return self.row == other.row and self.col == other.col and \
               self.player == other.player and self.is_queen == other.is_queen

    def __repr__(self):
        piece_type = 'K' if self.is_queen else 'M'
        player_info = 'TOP' if self.player == Player.PLAYER_TOP else 'BOT'
        representation = str((self.row, self.col)) + '(' + piece_type + '_' + player_info + ')'
        return representation

    @property
    def color(self):
        if self.player == Player.PLAYER_TOP:
            return PLAYER_TOP_COLOR
        elif self.player == Player.PLAYER_BOTTOM:
            return PLAYER_BOTTOM_COLOR

    @property
    def is_ready_to_promote(self) -> bool:
        if self.is_queen:
            return False
        if self.player == Player.PLAYER_BOTTOM and self.row == 0:
            return True
        if self.player == Player.PLAYER_TOP and self.row == ROWS-1:
            return True
        return False

    @property
    def position_on_display(self) -> tuple[int, int]:
        # Returns center of the square that piece is displayed on
        y = self.row * SQUARE_HEIGHT + SQUARE_HEIGHT//2
        x = self.col * SQUARE_WIDTH + SQUARE_WIDTH//2
        return x, y

    def promote(self):
        self.is_queen = True

    def move(self, row, col):
        self.row = row
        self.col = col

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.position_on_display, PIECE_RADIUS)
        if self.is_queen:
            pygame.draw.circle(window, CROWN_COLOR, self.position_on_display, PIECE_RADIUS // 2)

    def is_rival_piece(self, piece):
        return self.player != piece.player


