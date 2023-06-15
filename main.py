import pygame
from checkers.graphics_constants import FPS, WINDOW_WIDTH, WINDOW_HEIGHT, ICON_PATH, WINDOW_CAPTION
from checkers.Game import Game
from checkers.GameInterface import GameInterface


def set_display_window() -> pygame.Surface:
    window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    icon = pygame.image.load(ICON_PATH)
    pygame.display.set_icon(icon)
    pygame.display.set_caption(WINDOW_CAPTION)
    return window


def main():
    pygame.init()
    clock = pygame.time.Clock()
    window = set_display_window()
    game = Game(window)
    game_interface = GameInterface(game, window)

    running = True
    while running:
        clock.tick(FPS)

        game_interface.update_display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                game_interface.select(mouse_pos)

    pygame.quit()


if __name__ == '__main__':
    main()

