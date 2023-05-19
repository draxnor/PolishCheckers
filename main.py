import pygame
from checkers.constants import *
from checkers.Board import Board
from checkers.Player import Player

FPS = 60

def main():
    pygame.init()
    window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)
        board = Board()

        board.draw_background(window)
        board.draw_pieces(window)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

    pygame.quit()


if __name__ == '__main__':
    main()

