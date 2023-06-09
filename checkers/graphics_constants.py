from .game_constants import ROWS, COLUMNS

FPS = 60
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 1000
ICON_PATH = 'checkers/graphics/checkers_logo.png'
WINDOW_CAPTION = 'Polish Checkers by Paweł Mędyk'

SQUARE_WIDTH = WINDOW_WIDTH//COLUMNS
SQUARE_HEIGHT = WINDOW_HEIGHT//ROWS

PIECE_DIAMETER_TO_SQUARE_SIZE_RATIO = 3/4
PIECE_RADIUS = PIECE_DIAMETER_TO_SQUARE_SIZE_RATIO*min(SQUARE_WIDTH, SQUARE_HEIGHT)//2
MOVE_DOT_RADIUS = min(SQUARE_WIDTH, SQUARE_HEIGHT)//5

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 153)
LIGHT_GREEN = (144, 238, 144)

CHECKERBOARD_BACKGROUND_COLOR = BLACK
CHECKERBOARD_SQUARES_COLOR = WHITE
PLAYER_TOP_COLOR = RED
PLAYER_BOTTOM_COLOR = BLUE
CROWN_COLOR = YELLOW
HIGHLIGHT_COLOR = LIGHT_GREEN

