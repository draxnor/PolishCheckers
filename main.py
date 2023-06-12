import pygame
from checkers.constants import *
from checkers.Board import Board
from checkers.Game import Game

import sys
#temporary
from checkers.Piece import Piece
from checkers.Player import Player

FPS = 60

def get_piece_pos_from_mouse_pos(pos):
    x,y = pos
    row = y // SQUARE_HEIGHT
    col = x // SQUARE_WIDTH
    return row, col


def main():
    pygame.init()
    window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    clock = pygame.time.Clock()
    game = Game(window)

    print(sys.getsizeof(game.board.board))

    running = True
    while running:
        clock.tick(FPS)

        game.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_piece_pos_from_mouse_pos(mouse_pos)
                game.select(row, col)

    pygame.quit()


if __name__ == '__main__':
    main()

