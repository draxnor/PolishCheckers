import pygame
from checkers.constants import FPS, WINDOW_WIDTH, WINDOW_HEIGHT, SQUARE_HEIGHT, SQUARE_WIDTH
from checkers.Game import Game


def main():
    pygame.init()
    window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    pygame.display.set_caption('Polish Checkers by Paweł Mędyk')
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
                game.select(mouse_pos)

    pygame.quit()


if __name__ == '__main__':
    main()

