import pygame
from checkers.constants import FPS, WINDOW_WIDTH, WINDOW_HEIGHT, SQUARE_HEIGHT, SQUARE_WIDTH
from checkers.Game import Game


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

    running = True
    while running:
        clock.tick(FPS)

        game.update_display()
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

