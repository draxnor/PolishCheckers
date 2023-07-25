import pygame
from interface.ScreenLoops import set_display_window, display_main_menu


def main():
    pygame.init()
    clock = pygame.time.Clock()
    window = set_display_window()
    display_main_menu(window, clock)
    pygame.quit()


if __name__ == '__main__':
    main()