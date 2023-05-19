import pygame
from .constants import SQUARE_HEIGHT, SQUARE_WIDTH, \
    PLAYER1_COLOR, PLAYER2_COLOR, PIECE_RADIUS, CROWN_COLOR
from .Player import Player


class Piece:
    def __init__(self, row, col, player):
        self.row = row
        self.col = col
        self.player = player
        if player == Player.PLAYER1:
            self.color = PLAYER1_COLOR
        elif player == Player.PLAYER2:
            self.color = PLAYER2_COLOR
        self.is_king = False

    def get_position(self): # center of the square
        y = self.row * SQUARE_HEIGHT + SQUARE_HEIGHT//2
        x = self.col * SQUARE_WIDTH + SQUARE_WIDTH//2
        return x, y

    def promote_piece(self):
        self.is_king = True

    def get_possible_moves(self):
        pass

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.get_position(), PIECE_RADIUS)
        if self.is_king:
            pygame.draw.circle(window, CROWN_COLOR, self.get_position(), PIECE_RADIUS//2)

    def __repr__(self):
        if self.is_king is True:
            piece_info = 'K'
        else:
            piece_info = 'M'

        player_info = str(self.player.value) + 'P'
        representation = str((self.row,self.col))+'('+piece_info+'_'+player_info+')'
        return representation
