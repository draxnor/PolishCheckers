import pygame
from enum import Enum, auto
from interface.Button import Button
from graphics.graphics_constants import WINDOW_WIDTH, WINDOW_HEIGHT, MENU_BACKGROUND_COLOR


class MenuButtons(Enum):
    BUTTON_START = auto()
    BUTTON_OPTIONS = auto()
    BUTTON_EXIT = auto()


class Menu:
    def __init__(self, window: pygame.Surface):
        self.window = window
        buttons_width, buttons_height = 500, 128
        self.buttons = {MenuButtons.BUTTON_START: Button(WINDOW_WIDTH//2 - buttons_width//2,
                                                         WINDOW_HEIGHT//2 - buttons_height//2 - 200,
                                                         buttons_width, buttons_height, 'START'),
                        MenuButtons.BUTTON_OPTIONS: Button(WINDOW_WIDTH//2 - buttons_width//2,
                                                           WINDOW_HEIGHT//2 - buttons_height//2,
                                                           buttons_width, buttons_height, 'OPTIONS'),
                        MenuButtons.BUTTON_EXIT: Button(WINDOW_WIDTH//2 - buttons_width//2,
                                                        WINDOW_HEIGHT//2 - buttons_height//2 + 200,
                                                        buttons_width, buttons_height, 'EXIT')}

    def draw(self):
        self.window.fill(MENU_BACKGROUND_COLOR)
        for button in self.buttons.values():
            button.draw(self.window)

    def select(self, mouse_pos: tuple[int, int]) -> MenuButtons:
        for button in self.buttons.items():
            if button[1].does_collide(mouse_pos):
                return button[0]

