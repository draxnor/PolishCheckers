import pygame

FPS = 60
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
ROWS, COLUMNS = 10, 10
INITIAL_PIECE_COUNT = COLUMNS//2*(ROWS//2-1)
SQUARE_WIDTH = WINDOW_WIDTH//COLUMNS
SQUARE_HEIGHT = WINDOW_HEIGHT//ROWS

PIECE_DIAMETER_TO_SQUARE_SIZE_RATIO = 3/4
PIECE_RADIUS = PIECE_DIAMETER_TO_SQUARE_SIZE_RATIO*min(SQUARE_WIDTH, SQUARE_HEIGHT)//2
MOVE_DOT_RADIUS = min(SQUARE_WIDTH, SQUARE_HEIGHT)//5

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,153)
GREEN = (144, 238, 144)

PLAYER_TOP_COLOR = RED
PLAYER_BOTTOM_COLOR = BLUE
CROWN_COLOR = YELLOW
HIGHLIGHT_COLOR = GREEN

NONCAPTURE_QUEEN_MOVES_COUNT_LIMIT = 25
MOVES_COUNT_FOR_1V3_ENDGAME = 16*2
MOVES_COUNT_FOR_1V2_ENDGAME = 5*2
MOVES_COUNT_FOR_1V1_ENDGAME = 1
BOARD_STATE_REPETITION_LIMIT = 3
