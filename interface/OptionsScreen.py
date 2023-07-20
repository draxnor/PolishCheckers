import pygame
from enum import Enum, auto
from interface.Button import Button
from interface.TextInputBox import TextInputBox
from graphics.graphics_constants import WINDOW_WIDTH, WINDOW_HEIGHT, MENU_BACKGROUND_COLOR, MENU_TEXT_COLOR, \
    MENU_TEXT_SIZE, MENU_BUTTON_TEXT_SIZE
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


class OptionsScreen:
    def __init__(self, window: pygame.Surface, gameplay_options: GameplayOptions):
        self.window = window
        self.options = gameplay_options
        self.COLUMNS_TO_MIDDLE_DISTANCE = 150
        self.text_fields = self._init_text_fields()
        self.buttons = self._init_buttons()

        # self.update()

    def _init_text_fields(self):
        text_fields = {OptionsTextFields.STARTING_SIDE:
                           TextField((WINDOW_WIDTH // 2, 50), 'STARTING SIDE'),
                       OptionsTextFields.PLAYER_TOP_TYPE:
                           TextField((WINDOW_WIDTH // 2 - self.COLUMNS_TO_MIDDLE_DISTANCE, 250), 'PLAYER TOP'),
                       OptionsTextFields.PLAYER_BOTTOM_TYPE:
                           TextField((WINDOW_WIDTH // 2 + self.COLUMNS_TO_MIDDLE_DISTANCE, 250), 'PLAYER BOTTOM'),
                       OptionsTextFields.AI_TOP_LVL:
                           TextField((WINDOW_WIDTH // 2 - self.COLUMNS_TO_MIDDLE_DISTANCE, 550), 'AI DIFFICULTY'),
                       OptionsTextFields.AI_BOTTOM_LVL:
                           TextField((WINDOW_WIDTH // 2 + self.COLUMNS_TO_MIDDLE_DISTANCE, 550), 'AI DIFFICULTY')}
        return text_fields

    def _init_buttons(self):
        buttons_width, buttons_height, horizontal_distance, vertical_distance = 150, 100, 350, 10
        left_column_margin = WINDOW_WIDTH // 2 - buttons_width // 2 - self.COLUMNS_TO_MIDDLE_DISTANCE
        right_column_margin = WINDOW_WIDTH // 2 - buttons_width // 2 + self.COLUMNS_TO_MIDDLE_DISTANCE
        buttons = {OptionsButton.BUTTON_STARTING_SIDE_TOP:
                       Button(left_column_margin,
                              80,
                              buttons_width, buttons_height, 'TOP', text_size=32),
                   OptionsButton.BUTTON_STARTING_SIDE_BOTTOM:
                       Button(right_column_margin,
                              80,
                              buttons_width, buttons_height, 'BOTTOM', text_size=32),
                   OptionsButton.BUTTON_PLAYER_TOP_HUMAN:
                       Button(left_column_margin,
                              280,
                              buttons_width, buttons_height, 'HUMAN', text_size=32),
                   OptionsButton.BUTTON_PLAYER_TOP_AI:
                       Button(left_column_margin,
                              280 + buttons_height + vertical_distance,
                              buttons_width, buttons_height, 'AI', text_size=32),
                   OptionsButton.BUTTON_PLAYER_BOTTOM_HUMAN:
                       Button(right_column_margin,
                              280,
                              buttons_width, buttons_height, 'HUMAN', text_size=32),
                   OptionsButton.BUTTON_PLAYER_BOTTOM_AI:
                       Button(right_column_margin,
                              280 + buttons_height + vertical_distance,
                              buttons_width, buttons_height, 'AI', text_size=32),
                   OptionsButton.TEXTBOX_AI_TOP_LVL:
                       Button(left_column_margin,
                              580,
                              buttons_width, buttons_height, '5', text_size=32),
                   OptionsButton.TEXTBOX_AI_BOTTOM_LVL:
                       Button(right_column_margin,
                              580,
                              buttons_width, buttons_height, '4', text_size=32),
                   OptionsButton.BUTTON_GO_TO_MAIN_MENU:
                       Button(WINDOW_WIDTH // 2 - 500 // 2,
                              850,
                              500, buttons_height, 'GO TO MAIN MENU', text_size=32)
                   }
        return buttons

    def update(self):
        self._update_starting_player_buttons()
        self._update_starting_player_side()
        self._update_game_mode_buttons()
        self._update_ai_level_boxes()

    def _update_ai_level_boxes(self):
        pass #todo

    def _update_starting_player_side(self):
        player_side_buttons_keys = [OptionsButton.BUTTON_STARTING_PLAYER_COLOR_BOTTOM,
                                    OptionsButton.BUTTON_STARTING_PLAYER_COLOR_TOP]
        for key in player_side_buttons_keys:
            self.buttons[key].deactivate()
        if self.options.starting_player_side == PlayerSide.TOP:
            self.buttons[OptionsButton.BUTTON_STARTING_PLAYER_COLOR_TOP].activate()
        if self.options.starting_player_side == PlayerSide.BOTTOM:
            self.buttons[OptionsButton.BUTTON_STARTING_PLAYER_COLOR_BOTTOM].activate()

    def _update_starting_player_buttons(self):
        starting_player_buttons_keys = [OptionsButton.BUTTON_STARTING_PLAYER_1,
                                   OptionsButton.BUTTON_STARTING_PLAYER_2]
        for key in starting_player_buttons_keys:
            self.buttons[key].deactivate()

        if self.options.starting_player == PlayerNumbered.Player1:
            self.buttons[OptionsButton.BUTTON_STARTING_PLAYER_1].activate()
        if self.options.starting_player == PlayerNumbered.Player2:
            self.buttons[OptionsButton.BUTTON_STARTING_PLAYER_2].activate()


    def _update_game_mode_buttons(self):
        game_mode_buttons_keys = [OptionsButton.BUTTON_GAME_MODE_PVP,
                             OptionsButton.BUTTON_GAME_MODE_PVAI,
                             OptionsButton.BUTTON_GAME_MODE_AIVAI]
        for key in game_mode_buttons_keys:
            self.buttons[key].deactivate()
        if self.options.game_mode == GameMode.Human_vs_Human:
            self.buttons[OptionsButton.BUTTON_GAME_MODE_PVP].activate()
        if self.options.game_mode == GameMode.Human_vs_AI:
            self.buttons[OptionsButton.BUTTON_GAME_MODE_PVAI].activate()
        if self.options.game_mode == GameMode.AI_vs_AI:
            self.buttons[OptionsButton.BUTTON_GAME_MODE_AIVAI].activate()

    def draw(self):
        self.window.fill(MENU_BACKGROUND_COLOR)
        for button in self.buttons.values():
            button.draw(self.window)
        for text_field in self.text_fields.values():
            text_field.draw(self.window)

    def select(self, mouse_pos: tuple[int, int]) -> OptionsButton:
        for button in self.buttons.items():
            if button[1].does_collide(mouse_pos):
                return button[0]

    def get_options(self):
        return self.options

    def process(self, button: OptionsButton):
        pass #todo
