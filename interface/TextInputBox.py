import sys
import pygame
from interface.Button import Button
from graphics.graphics_constants import BUTTON_BG_COLOR, BUTTON_TEXT_COLOR, MENU_BUTTON_TEXT_SIZE, \
    WINDOW_WIDTH, WINDOW_HEIGHT, BUTTON_BG_HIGHLIGHT_COLOR


class TextInputBox(Button):
    def __init__(self, left, top, width, height, text: str = '',
                 bg_color: tuple[int, int, int] = BUTTON_BG_COLOR,
                 text_color: tuple[int, int, int] = BUTTON_TEXT_COLOR,
                 font: str | None = None,
                 text_size: int = MENU_BUTTON_TEXT_SIZE,
                 is_active: bool = False,
                 is_visible: bool = True,
                 bg_highlight_color: tuple[int, int, int] = BUTTON_BG_HIGHLIGHT_COLOR,
                 is_digit_only: bool = False,
                 max_text_length: int = 1) -> None:
        self.temp_text = ''
        self.is_digit_only = is_digit_only
        self.max_text_length = max_text_length
        super().__init__(left, top, width, height, text, bg_color, text_color, font, text_size,
                         is_active, is_visible, bg_highlight_color)

    def add_character(self, new_char: str):
        if len(new_char) > 1:
            print('Warning: Adding more than 1 character to TextBox at a time.', file=sys.stderr)
        self.temp_text += new_char

    def remove_character(self):
        if len(self.text) > 0:
            self.temp_text = self.temp_text[:-1]

    def confirm_text_changes(self):
        if self.temp_text == '':
            self.reject_text_changes()
            return self.text
        if len(self.temp_text) > self.max_text_length:
            self.temp_text = self.temp_text[0:self.max_text_length]
        if self.is_digit_only:
            if not self.temp_text.isdigit():
                self.reject_text_changes()
                return self.text
        self.text = self.temp_text
        self.temp_text = ''
        self.deactivate()
        return self.text

    def reject_text_changes(self):
        self.temp_text = ''
        self.deactivate()

    def process_keydown(self, event: pygame.event.Event):
        if not self.is_active:
            return self.text
        if event.key == pygame.K_RETURN:
            self.confirm_text_changes()
        if event.key == pygame.K_ESCAPE:
            self.reject_text_changes()
        if event.key == pygame.K_BACKSPACE:
            self.remove_character()
        if event.unicode.isprintable():
            self.add_character(event.unicode)
        return self.text

    def draw(self, window: pygame.Surface):
        if not self.is_visible:
            return
        if self.is_active:
            bg_color = self.bg_highlight_color
            displayed_text = self.temp_text + '|'
        else:
            bg_color = self.bg_color
            displayed_text = self.text
        pygame.draw.rect(window, bg_color, pygame.Rect(self.left, self.top, self.width, self.height))
        if displayed_text != '':
            button_center = self.left + self.width // 2, self.top + self.height // 2
            font_obj = pygame.font.SysFont(self.font, self.text_size)
            text_img = font_obj.render(displayed_text, True, BUTTON_TEXT_COLOR)
            left = min(WINDOW_WIDTH - text_img.get_width(), max(0, button_center[0] - text_img.get_width() // 2))
            top = min(WINDOW_HEIGHT - text_img.get_height(), max(0, button_center[1] - text_img.get_height() // 2))
            window.blit(text_img, (left, top))

    def clear(self):
        self.temp_text = ''
