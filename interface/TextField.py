import pygame
from graphics.graphics_constants import WINDOW_WIDTH, WINDOW_HEIGHT, MENU_TEXT_SIZE, MENU_TEXT_COLOR


class TextField:
    def __init__(self,
                 center: tuple[int, int],
                 text: str = '',
                 text_color: tuple[int, int, int] = MENU_TEXT_COLOR,
                 font: str | None = None,
                 text_size: int = MENU_TEXT_SIZE,
                 is_visible: bool = True) -> None:
        self.text_center = center
        self.text = text
        self.text_color = text_color
        self.font = font
        self.text_size = text_size
        self.is_visible = is_visible

    def draw(self, window: pygame.Surface):
        if not self.is_visible:
            return
        if self.text != '':
            font_obj = pygame.font.SysFont(self.font, self.text_size)
            text_img = font_obj.render(self.text, True, self.text_color)
            left = min(WINDOW_WIDTH-text_img.get_width(), max(0, self.text_center[0] - text_img.get_width()//2))
            top = min(WINDOW_HEIGHT-text_img.get_height(), max(0, self.text_center[1] - text_img.get_height()//2))
            window.blit(text_img, (left, top))

    def get_text(self):
        return self.text

    def set_text(self, new_text: str):
        self.text = new_text

    def hide(self):
        self.is_visible = False

    def unhide(self):
        self.is_visible = True

