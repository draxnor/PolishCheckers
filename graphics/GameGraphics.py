import pygame
from checkers.Player import Player
from checkers.Board import Board
from checkers.Piece import Piece
from checkers.SequenceOfMoves import SequenceOfMoves
from checkers.Move import Move
from checkers.game_constants import ROWS, COLUMNS
from .graphics_constants import PIECE_RADIUS, SQUARE_HEIGHT, SQUARE_WIDTH, HIGHLIGHT_COLOR, \
    MOVE_DOT_RADIUS, CHECKERBOARD_BACKGROUND_COLOR, CHECKERBOARD_SQUARES_COLOR, \
    WINDOW_WIDTH, PLAYER_BOTTOM_COLOR, PLAYER_TOP_COLOR, \
    GAME_OVER_MESSAGE_COLOR, CROWN_IMG_PATH, GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT, \
    PLAYER_TOP_COLOR_NAME, PLAYER_BOTTOM_COLOR_NAME, TURN_INFO_TEXT_SIZE, TURN_INFO_TEXT_COLOR, TURN_INFO_POS,\
    GAME_WINDOW_HORIZONTAL_OFFSET, GAME_WINDOW_VERTICAL_OFFSET, \
    PREVIOUS_PIECE_POSITION_COLOR, LAST_PERFORMED_SEQUENCE_COLOR
from checkers.Game import Game


class GameGraphics:
    def __init__(self, main_window: pygame.Surface) -> None:
        self.main_window = main_window
        self.window = pygame.Surface([GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT])

    def clear_main_window(self):
        self.main_window.fill(CHECKERBOARD_BACKGROUND_COLOR)

    def draw_game_window_on_main_window(self):
        self.main_window.blit(self.window, (GAME_WINDOW_HORIZONTAL_OFFSET, GAME_WINDOW_VERTICAL_OFFSET))

    def draw_turn_information(self, turn: Player, is_human_turn: bool):
        if turn == Player.PLAYER_TOP:
            turn_info = 'Player: ' + PLAYER_TOP_COLOR_NAME + ' (TOP)'
        else:
            turn_info = 'Player: ' + PLAYER_BOTTOM_COLOR_NAME + ' (BOTTOM)'
        player_type_info = 'Type: ' + ('Human' if is_human_turn else 'AI')
        font = pygame.font.Font(None, TURN_INFO_TEXT_SIZE)

        turn_text = font.render(turn_info, True, TURN_INFO_TEXT_COLOR)
        player_type_text = font.render(player_type_info, True, TURN_INFO_TEXT_COLOR)

        turn_text_rect = turn_text.get_rect(x=TURN_INFO_POS[0], y=TURN_INFO_POS[1])
        player_type_text_rect = player_type_text.get_rect(x=TURN_INFO_POS[0] + WINDOW_WIDTH // 2, y=TURN_INFO_POS[1])
        self.main_window.blit(turn_text, turn_text_rect)
        self.main_window.blit(player_type_text, player_type_text_rect)

    def draw_valid_moves_of_selected_piece(self, game: Game, selected_piece: Piece) -> None:
        piece_valid_sequences = game.get_valid_sequences_of_a_piece(selected_piece)
        for sequence in piece_valid_sequences:
            self.draw_sequence(sequence)
            self.draw_first_move_in_sequence_highlight(sequence)

    def draw_piece(self, piece: Piece) -> None:
        piece_position_on_screen = self.get_piece_position_on_game_window(piece)
        pygame.draw.circle(self.window, self.get_piece_color(piece), piece_position_on_screen, PIECE_RADIUS)
        if piece.is_queen:
            crown_img = pygame.image.load(CROWN_IMG_PATH)
            crown_img = pygame.transform.scale_by(crown_img, (1 / 16, 1 / 16))
            img_size = crown_img.get_size()
            self.window.blit(crown_img,
                             (piece_position_on_screen[0] - img_size[0] // 2,
                              piece_position_on_screen[1] - img_size[1] // 2))
            # pygame.draw.circle(self.window, CROWN_COLOR, piece_position_on_screen, PIECE_RADIUS // 2)

    def draw_sequence(self, sequence: SequenceOfMoves) -> None:
        for move in sequence.sequence:
            self.draw_move_dot_hint(move)

    def draw_first_move_in_sequence_highlight(self, sequence: SequenceOfMoves, position: int = 0) -> None:
        self.draw_move_highlight(sequence.sequence[-position - 1])

    def draw_move_dot_hint(self, move: Move) -> None:
        destination_row, destination_col = move.destination
        destination_square_center = (destination_col * SQUARE_WIDTH + SQUARE_WIDTH // 2,
                                     destination_row * SQUARE_HEIGHT + SQUARE_HEIGHT // 2)
        pygame.draw.circle(self.window, HIGHLIGHT_COLOR, destination_square_center, MOVE_DOT_RADIUS)

    def draw_move_highlight(self, move: Move) -> None:
        destination_row, destination_col = move.destination
        square = pygame.Rect((destination_col * SQUARE_WIDTH, destination_row * SQUARE_HEIGHT),
                             (SQUARE_WIDTH, SQUARE_HEIGHT))
        pygame.draw.rect(self.window, HIGHLIGHT_COLOR, square)

    def draw_square(self, row: int, col: int, color: tuple[int, int, int]) -> None:
        pygame.draw.rect(self.window, color, pygame.Rect((col * SQUARE_WIDTH, row * SQUARE_HEIGHT),
                                                         (SQUARE_WIDTH, SQUARE_HEIGHT)))

    def draw_background(self) -> None:
        self.window.fill(CHECKERBOARD_BACKGROUND_COLOR)
        for row in range(ROWS):
            for col in range(COLUMNS):
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                    self.draw_square(row, col, CHECKERBOARD_SQUARES_COLOR)

    def draw_empty_board(self) -> None:
        self.draw_background()
        self.draw_pieces()

    def draw_pieces(self, board: Board) -> None:
        for row in range(ROWS):
            for col in range(COLUMNS):
                field_content = board.get_piece(row, col)
                if isinstance(field_content, Piece):
                    self.draw_piece(field_content)

    def draw_multiple_sequences(self, valid_sequences: list[SequenceOfMoves]) -> None:
        # Only for custom visualisation and debugging
        for sequence in valid_sequences:
            self.draw_sequence(sequence)

    def draw_gameover_message(self, game: Game):
        main_message_font_size = 128
        instruction_font_size = 48
        distance_between_lines = 50
        distance_between_lines_instructions = 30
        gameover_messages = {'ONGOING': ['Game is still in progress.'],
                             'PLAYER_TOP_WON': ['GAME OVER', PLAYER_TOP_COLOR_NAME + ' PLAYER WON'],
                             'PLAYER_BOTTOM_WON': ['GAME OVER', PLAYER_BOTTOM_COLOR_NAME + ' PLAYER WON'],
                             'DRAW': ['GAME OVER', 'DRAW']}
        instructions = ['Click anywhere to go to main menu', 'Click SPACE to restart game']

        main_message = gameover_messages[game.state.name]
        main_message_height = (len(main_message) - 1) * distance_between_lines + \
                              len(main_message) * main_message_font_size

        for i, line in enumerate(main_message):
            font = pygame.font.Font(None, main_message_font_size)
            game_over_text = font.render(line, True, GAME_OVER_MESSAGE_COLOR)
            line_height = game_over_text.get_height()
            line_vertical_center = GAME_WINDOW_HEIGHT // 2 - main_message_height // 2 + main_message_font_size // 2 + \
                                   i * (line_height + distance_between_lines)
            text_rect = game_over_text.get_rect(center=(GAME_WINDOW_WIDTH // 2, line_vertical_center))
            self.window.blit(game_over_text, text_rect)

        for i, line in enumerate(instructions):
            font = pygame.font.Font(None, instruction_font_size)
            instruction_text = font.render(line, True, GAME_OVER_MESSAGE_COLOR)
            line_vertical_center = GAME_WINDOW_HEIGHT // 2 + main_message_height // 2 + \
                                   i * (instruction_font_size + distance_between_lines_instructions)
            text_rect = instruction_text.get_rect(center=(GAME_WINDOW_WIDTH // 2, line_vertical_center))
            self.window.blit(instruction_text, text_rect)

    def get_piece_position_on_game_window(self, piece: Piece) -> tuple[int, int]:
        x = piece.col * SQUARE_WIDTH + SQUARE_WIDTH // 2
        y = piece.row * SQUARE_HEIGHT + SQUARE_HEIGHT // 2
        return x, y

    def get_piece_color(self, piece: Piece) -> tuple[int, int, int]:
        if piece.player == Player.PLAYER_TOP:
            return PLAYER_TOP_COLOR
        elif piece.player == Player.PLAYER_BOTTOM:
            return PLAYER_BOTTOM_COLOR

    def draw_last_executed_sequence(self, seq: SequenceOfMoves) -> None:
        self.draw_square(*seq.first_move.origin, PREVIOUS_PIECE_POSITION_COLOR)
        for move in seq.sequence:
            self.draw_square(*move.destination, LAST_PERFORMED_SEQUENCE_COLOR)

