import pygame
from .constants import SQUARE_HEIGHT, SQUARE_WIDTH, \
    PLAYER_TOP_COLOR, PLAYER_BOTTOM_COLOR, PIECE_RADIUS, CROWN_COLOR, \
    ROWS, COLUMNS
from .Player import Player


class Piece:
    def __init__(self, row, col, player: Player):
        self.row = row
        self.col = col
        self.player = player
        if player == Player.PLAYER_TOP:
            self.color = PLAYER_TOP_COLOR
        elif player == Player.PLAYER_BOTTOM:
            self.color = PLAYER_BOTTOM_COLOR
        self.is_queen = False

    def get_position(self): # center of the square
        y = self.row * SQUARE_HEIGHT + SQUARE_HEIGHT//2
        x = self.col * SQUARE_WIDTH + SQUARE_WIDTH//2
        return x, y

    def promote_piece(self):
        self.is_queen = True

    def move(self, row, col):
        self.row = row
        self.col = col

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.get_position(), PIECE_RADIUS)
        if self.is_queen:
            pygame.draw.circle(window, CROWN_COLOR, self.get_position(), PIECE_RADIUS//2)

    def is_rival_piece(self, piece):
        return self.player != piece.player

    def __repr__(self):
        if self.is_queen is True:
            piece_info = 'K'
        else:
            piece_info = 'M'
        player_info =  'P' + str(self.player.value)
        representation = str((self.row,self.col)) + '(' + piece_info + '_' + player_info + ')'
        return representation
