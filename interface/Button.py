import pygame

from graphics.graphics_constants import BUTTON_BG_COLOR, BUTTON_TEXT_COLOR, MENU_BUTTON_TEXT_SIZE, \
    WINDOW_WIDTH, WINDOW_HEIGHT, BUTTON_BG_HIGHLIGHT_COLOR


class Button:
    def __init__(self, left, top, width, height, text: str = '',
                 bg_color: tuple[int, int, int] = BUTTON_BG_COLOR,
                 text_color: tuple[int, int, int] = BUTTON_TEXT_COLOR,
                 font: str | None = None,
                 text_size: int = MENU_BUTTON_TEXT_SIZE,
                 is_active: bool = False,
                 is_visible: bool = True,
                 bg_highlight_color: tuple[int, int, int] = BUTTON_BG_HIGHLIGHT_COLOR) -> None:
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = font
        self.text_size = text_size
        self.is_active = is_active
        self.is_visible = is_visible
        self.bg_highlight_color = bg_highlight_color

    def does_collide(self, mouse_pos: tuple[int, int]) -> bool:
        return self.left <= mouse_pos[0] <= self.left + self.width and \
            self.top <= mouse_pos[1] <= self.top + self.height

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def draw(self, window: pygame.Surface):
        if not self.is_visible:
            return
        if self.is_active:
            bg_color = self.bg_highlight_color
        else:
            bg_color = self.bg_color
        pygame.draw.rect(window, bg_color, pygame.Rect(self.left, self.top, self.width, self.height))
        if self.text != '':
            button_center = self.left + self.width//2, self.top + self.height//2
            font_obj = pygame.font.SysFont(self.font, self.text_size)
            text_img = font_obj.render(self.text, True, self.text_color)
            left = min(WINDOW_WIDTH-text_img.get_width(), max(0, button_center[0] - text_img.get_width()//2))
            top = min(WINDOW_HEIGHT-text_img.get_height(), max(0, button_center[1] - text_img.get_height()//2))
            window.blit(text_img, (left, top))

    def select(self):
        if self.is_active:
            self.deactivate()
        else:
            self.activate()

    def get_text(self):
        return self.text

    def set_text(self, new_text: str):
        self.text = new_text

    def make_visible(self):
        self.is_visible = True

    def make_hidden(self):
        self.is_visible = False

