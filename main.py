import pygame
from graphics.graphics_constants\
    import FPS, WINDOW_WIDTH, WINDOW_HEIGHT, ICON_PATH, WINDOW_CAPTION, MENU_BACKGROUND_COLOR
from checkers.Game import Game
from interface.GameInterface import GameInterface, SelectionStatus
from interface.Menu import MenuButtons, Menu
from interface.GameplayOptions import GameplayOptions
from interface.OptionsScreen import OptionsScreen, OptionsButton


def set_display_window() -> pygame.Surface:
    window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    icon = pygame.image.load(ICON_PATH)
    pygame.display.set_icon(icon)
    pygame.display.set_caption(WINDOW_CAPTION)
    return window


def display_options_screen(window: pygame.Surface, clock: pygame.time.Clock, gameplay_options: GameplayOptions) -> bool:
    options_screen = OptionsScreen(window, gameplay_options)
    running = True
    while running:
        clock.tick(FPS)
        options_screen.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_selected = options_screen.select(mouse_pos)
                if button_selected == OptionsButton.BUTTON_GO_TO_MAIN_MENU:
                    running = False
                else:
                    options_screen.process(button_selected)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False
    return True


def display_main_menu(window: pygame.Surface, clock: pygame.time.Clock):
    menu = Menu(window)
    gameplay_options = GameplayOptions()
    running = True
    was_closed_normally = display_options_screen(window, clock, gameplay_options) #todo to delete
    while running:
        clock.tick(FPS)
        menu.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_selected = menu.select(mouse_pos)
                if button_selected == MenuButtons.BUTTON_START:
                    was_closed_normally = display_game(window, clock, gameplay_options)
                    if not was_closed_normally:
                        return
                if button_selected == MenuButtons.BUTTON_OPTIONS:
                    was_closed_normally = display_options_screen(window, clock, gameplay_options)
                    if not was_closed_normally:
                        return
                if button_selected == MenuButtons.BUTTON_EXIT:
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False


def display_game(window: pygame.Surface, clock: pygame.time.Clock, gameplay_options: GameplayOptions) -> bool:
    game = Game()
    game_interface = GameInterface(game, window)

    running = True
    while running:
        clock.tick(FPS)
        game_interface.update_display()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                status = game_interface.select(mouse_pos)
                if status == SelectionStatus.GAMEOVER:
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_interface.reset()
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                return False
    return True


def main():
    pygame.init()
    clock = pygame.time.Clock()
    window = set_display_window()
    display_main_menu(window, clock)
    pygame.quit()


if __name__ == '__main__':
    main()

