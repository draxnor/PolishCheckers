import sys

import pygame
from enum import Enum, auto
from interface.Button import Button
from interface.TextInputBox import TextInputBox
from graphics.graphics_constants import WINDOW_WIDTH, WINDOW_HEIGHT, MENU_BACKGROUND_COLOR, MENU_TEXT_COLOR, \
    MENU_TEXT_SIZE, MENU_BUTTON_TEXT_SIZE, OPTIONS_TEXT_SIZE
from interface.GameplayOptions import GameplayOptions, PlayerType, PlayerSide
from interface.TextField import TextField


class OptionsButton(Enum):
    BUTTON_STARTING_SIDE_TOP = auto()
    BUTTON_STARTING_SIDE_BOTTOM = auto()
    BUTTON_PLAYER_TOP_HUMAN = auto()
    BUTTON_PLAYER_TOP_AI = auto()
    BUTTON_PLAYER_BOTTOM_HUMAN = auto()
    BUTTON_PLAYER_BOTTOM_AI = auto()
    TEXTBOX_AI_TOP_LVL = auto()
    TEXTBOX_AI_BOTTOM_LVL = auto()
    BUTTON_GO_TO_MAIN_MENU = auto()


class OptionsTextFields(Enum):
    STARTING_SIDE = auto()
    PLAYER_TOP_TYPE = auto()
    PLAYER_BOTTOM_TYPE = auto()
    AI_TOP_LVL = auto()
    AI_BOTTOM_LVL = auto()
    AI_LVL_HINT = auto()
    AI_LVL_HINT2 = auto()


class OptionsScreen:
    def __init__(self, window: pygame.Surface, gameplay_options: GameplayOptions):
        self.window = window
        self.options = gameplay_options
        self.COLUMNS_TO_MIDDLE_DISTANCE = 150
        self.text_fields = self._init_text_fields()
        self.buttons = self._init_buttons()
        self.update()
        self.selected = None

    def _init_text_fields(self):
        text_fields = {OptionsTextFields.STARTING_SIDE:
                           TextField((WINDOW_WIDTH // 2, 50), 'STARTING SIDE'),
                       OptionsTextFields.PLAYER_TOP_TYPE:
                           TextField((WINDOW_WIDTH // 2 - self.COLUMNS_TO_MIDDLE_DISTANCE, 250),
                                     'PLAYER TOP'),
                       OptionsTextFields.PLAYER_BOTTOM_TYPE:
                           TextField((WINDOW_WIDTH // 2 + self.COLUMNS_TO_MIDDLE_DISTANCE, 250),
                                     'PLAYER BOTTOM'),
                       OptionsTextFields.AI_TOP_LVL:
                           TextField((WINDOW_WIDTH // 2 - self.COLUMNS_TO_MIDDLE_DISTANCE, 550),
                                     'AI DIFFICULTY'),
                       OptionsTextFields.AI_BOTTOM_LVL:
                           TextField((WINDOW_WIDTH // 2 + self.COLUMNS_TO_MIDDLE_DISTANCE, 550),
                                     'AI DIFFICULTY'),
                       OptionsTextFields.AI_LVL_HINT:
                           TextField((WINDOW_WIDTH // 2, 720),
                                     'Difficulty from 1 to 10.', text_size=OPTIONS_TEXT_SIZE),
                       OptionsTextFields.AI_LVL_HINT2:
                           TextField((WINDOW_WIDTH // 2, 750),
                                     'For difficulty higher than 6, computations may take a while!',
                                     text_size=OPTIONS_TEXT_SIZE)}
        return text_fields

    def _init_buttons(self):
        buttons_width, buttons_height, horizontal_distance, vertical_distance = 150, 100, 350, 10
        left_column_margin = WINDOW_WIDTH // 2 - buttons_width // 2 - self.COLUMNS_TO_MIDDLE_DISTANCE
        right_column_margin = WINDOW_WIDTH // 2 - buttons_width // 2 + self.COLUMNS_TO_MIDDLE_DISTANCE
        buttons = {OptionsButton.BUTTON_STARTING_SIDE_TOP:
                       Button(left_column_margin,
                              80,
                              buttons_width, buttons_height, 'TOP', text_size=OPTIONS_TEXT_SIZE),
                   OptionsButton.BUTTON_STARTING_SIDE_BOTTOM:
                       Button(right_column_margin,
                              80,
                              buttons_width, buttons_height, 'BOTTOM', text_size=OPTIONS_TEXT_SIZE),
                   OptionsButton.BUTTON_PLAYER_TOP_HUMAN:
                       Button(left_column_margin,
                              280,
                              buttons_width, buttons_height, 'HUMAN', text_size=OPTIONS_TEXT_SIZE),
                   OptionsButton.BUTTON_PLAYER_TOP_AI:
                       Button(left_column_margin,
                              280 + buttons_height + vertical_distance,
                              buttons_width, buttons_height, 'AI', text_size=OPTIONS_TEXT_SIZE),
                   OptionsButton.BUTTON_PLAYER_BOTTOM_HUMAN:
                       Button(right_column_margin,
                              280,
                              buttons_width, buttons_height, 'HUMAN', text_size=OPTIONS_TEXT_SIZE),
                   OptionsButton.BUTTON_PLAYER_BOTTOM_AI:
                       Button(right_column_margin,
                              280 + buttons_height + vertical_distance,
                              buttons_width, buttons_height, 'AI', text_size=OPTIONS_TEXT_SIZE),
                   OptionsButton.TEXTBOX_AI_TOP_LVL:
                       TextInputBox(left_column_margin,
                              580,
                              buttons_width, buttons_height, '5', text_size=OPTIONS_TEXT_SIZE,
                                    is_digit_only=True, max_text_length=1),
                   OptionsButton.TEXTBOX_AI_BOTTOM_LVL:
                       TextInputBox(right_column_margin,
                              580,
                              buttons_width, buttons_height, '4', text_size=OPTIONS_TEXT_SIZE,
                                    is_digit_only=True, max_text_length=1),
                   OptionsButton.BUTTON_GO_TO_MAIN_MENU:
                       Button(WINDOW_WIDTH // 2 - 500 // 2,
                              850,
                              500, buttons_height, 'GO TO MAIN MENU', text_size=OPTIONS_TEXT_SIZE)
                   }
        return buttons

    def deactivate_all(self):
        for button in self.buttons.values():
            button.deactivate()

    def update(self):
        self._update_starting_side_button()
        self._update_player_type_buttons()
        self._update_ai_lvl_boxes()

    def _update_ai_lvl_boxes(self):
        if self.options.top_player_type == PlayerType.Human:
            self.buttons[OptionsButton.TEXTBOX_AI_TOP_LVL].hide()
            self.text_fields[OptionsTextFields.AI_TOP_LVL].hide()
        else:
            self.buttons[OptionsButton.TEXTBOX_AI_TOP_LVL].unhide()
            self.text_fields[OptionsTextFields.AI_TOP_LVL].unhide()
        if self.options.bottom_player_type == PlayerType.Human:
            self.buttons[OptionsButton.TEXTBOX_AI_BOTTOM_LVL].hide()
            self.text_fields[OptionsTextFields.AI_BOTTOM_LVL].hide()
        else:
            self.buttons[OptionsButton.TEXTBOX_AI_BOTTOM_LVL].unhide()
            self.text_fields[OptionsTextFields.AI_BOTTOM_LVL].unhide()
        if self.options.bottom_player_type == PlayerType.Human and self.options.top_player_type == PlayerType.Human:
            self.text_fields[OptionsTextFields.AI_LVL_HINT].hide()
            self.text_fields[OptionsTextFields.AI_LVL_HINT2].hide()
        else:
            self.text_fields[OptionsTextFields.AI_LVL_HINT].unhide()
            self.text_fields[OptionsTextFields.AI_LVL_HINT2].unhide()

    def _update_starting_side_button(self):
        player_type_buttons = [OptionsButton.BUTTON_STARTING_SIDE_TOP,
                               OptionsButton.BUTTON_STARTING_SIDE_BOTTOM]
        for key in player_type_buttons:
            self.buttons[key].deactivate()
        if self.options.starting_side == PlayerSide.TOP:
            self.buttons[OptionsButton.BUTTON_STARTING_SIDE_TOP].activate()
        if self.options.starting_side == PlayerSide.BOTTOM:
            self.buttons[OptionsButton.BUTTON_STARTING_SIDE_BOTTOM].activate()

    def _update_player_type_buttons(self):
        player_type_buttons = [OptionsButton.BUTTON_PLAYER_TOP_HUMAN,
                               OptionsButton.BUTTON_PLAYER_TOP_AI,
                               OptionsButton.BUTTON_PLAYER_BOTTOM_HUMAN,
                               OptionsButton.BUTTON_PLAYER_BOTTOM_AI]
        for key in player_type_buttons:
            self.buttons[key].deactivate()
        if self.options.top_player_type == PlayerType.Human:
            self.buttons[OptionsButton.BUTTON_PLAYER_TOP_HUMAN].activate()
        else:
            self.buttons[OptionsButton.BUTTON_PLAYER_TOP_AI].activate()
        if self.options.bottom_player_type == PlayerType.Human:
            self.buttons[OptionsButton.BUTTON_PLAYER_BOTTOM_HUMAN].activate()
        else:
            self.buttons[OptionsButton.BUTTON_PLAYER_BOTTOM_AI].activate()

    def draw(self):
        self.window.fill(MENU_BACKGROUND_COLOR)
        for button in self.buttons.values():
            button.draw(self.window)
        for text_field in self.text_fields.values():
            text_field.draw(self.window)

    def select(self, mouse_pos: tuple[int, int]) -> OptionsButton:
        button_selected = None
        self.selected = None
        self.deactivate_all()
        for button in self.buttons.items():
            if button[1].does_collide(mouse_pos):
                button_selected = button[0]
                self.selected = button[0]
                break
        self.process_selection()
        self.update()
        return button_selected

    def get_options(self):
        return self.options

    def process_selection(self):
        if self.selected is None:
            return
        if self.selected == OptionsButton.BUTTON_STARTING_SIDE_TOP:
            self.options.set_starting_side(PlayerSide.TOP)
        if self.selected == OptionsButton.BUTTON_STARTING_SIDE_BOTTOM:
            self.options.set_starting_side(PlayerSide.BOTTOM)
        if self.selected == OptionsButton.BUTTON_PLAYER_TOP_HUMAN:
            self.options.set_top_player_type(PlayerType.Human)
        if self.selected == OptionsButton.BUTTON_PLAYER_TOP_AI:
            self.options.set_top_player_type(PlayerType.AI)
        if self.selected == OptionsButton.BUTTON_PLAYER_BOTTOM_HUMAN:
            self.options.set_bottom_player_type(PlayerType.Human)
        if self.selected == OptionsButton.BUTTON_PLAYER_BOTTOM_AI:
            self.options.set_bottom_player_type(PlayerType.AI)
        if self.selected == OptionsButton.BUTTON_GO_TO_MAIN_MENU:
            pass
        if self.selected == OptionsButton.TEXTBOX_AI_BOTTOM_LVL or self.selected == OptionsButton.TEXTBOX_AI_TOP_LVL:
            if self.buttons[self.selected].is_hidden():
                self.selected = None
            else:
                self.buttons[self.selected].activate()
                self.buttons[self.selected].clear()
        else:
            self.selected = None

    def process_keyboard_input(self, event: pygame.event.Event) -> bool:
        if not self.selected == OptionsButton.TEXTBOX_AI_BOTTOM_LVL \
                and not self.selected == OptionsButton.TEXTBOX_AI_TOP_LVL:
            if event.key == pygame.K_ESCAPE:
                return False
            else:
                return True
        try:
            self.buttons[self.selected].process_keydown(event)
            return True
        except AttributeError:
            print('Cannot reject text changes in "OptionsScreen.process_keyboard_input()"', file=sys.stderr)


