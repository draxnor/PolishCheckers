import pygame
from checkers.constants import *
from checkers.Board import Board
from checkers.Game import Game

import sys
#temporary
from checkers.Piece import Piece
from checkers.Player import Player

FPS = 60

def get_piece_pos_from_mouse_pos(pos):
    x,y = pos
    row = y // SQUARE_HEIGHT
    col = x // SQUARE_WIDTH
    return row, col


def main():
    pygame.init()
    window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    clock = pygame.time.Clock()
    game = Game(window)

    for row in range(ROWS):
        for col in range(COLUMNS):
            game.board.board[row][col] = 0
    game.board.board[6][5] = Piece(6, 5, Player.PLAYER_BOTTOM)
    game.board.board[6][5].promote()
    # # game.board.board[2][5] = Piece(2, 5, Player.PLAYER_BOTTOM)
    game.board.board[4][5] = Piece(4, 5, Player.PLAYER_BOTTOM)
    game.board.board[4][3] = Piece(4, 3, Player.PLAYER_BOTTOM)
    # game.board.board[1][4] = Piece(1, 4, Player.PLAYER_TOP)
    # # game.board.board[1][4].promote()
    # game.board.board[2][5] = Piece(2, 5, Player.PLAYER_BOTTOM)
    # game.board.board[4][5] = Piece(4, 5, Player.PLAYER_BOTTOM)
    # game.board.board[4][3] = Piece(4, 3, Player.PLAYER_TOP)
    # # game.board.board[2][3] = Piece(2, 3, Player.PLAYER_BOTTOM)
    # game.board.board[4][9] = Piece(4, 9, Player.PLAYER_TOP)
    game.board.board[5][8] = Piece(5, 8, Player.PLAYER_TOP)
    game.board.board[5][8].promote()
    game.set_new_turn()
    game.board.recalculate_pieces_count()

    running = True
    while running:
        clock.tick(FPS)

        game.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_piece_pos_from_mouse_pos(mouse_pos)
                game.select(row, col)

    pygame.quit()


if __name__ == '__main__':
    main()

