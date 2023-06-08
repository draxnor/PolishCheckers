import unittest
from checkers.Player import Player
from checkers.Piece import Piece
from checkers.Board import Board
from checkers.Move import Move
from checkers.constants import *


class TestBoard(unittest.TestCase):
    def test_get_piece(self):
        board = Board()
        self.assertEqual(board.get_piece(0, 0), -1)
        self.assertIsInstance(board.get_piece(0, 1), Piece)
        self.assertEqual(board.get_piece(4, 1), 0)

    def test__is_out_of_bound(self):
        board = Board()
        self.assertTrue(board._is_out_of_bound(-1,0))
        self.assertTrue(board._is_out_of_bound(5, -1))
        self.assertTrue(board._is_out_of_bound(ROWS, 0))
        self.assertTrue(board._is_out_of_bound(9, COLUMNS))
        self.assertFalse(board._is_out_of_bound(9, 9))

    def test_get_possible_noncapture_moves_for_man(self):
        board = Board()
        piece = board.get_piece(0,1)
        moves = board.get_potential_noncapture_sequences_for_man(piece)
        self.assertListEqual(moves, [])

        piece2 = board.get_piece(3, 0)
        moves2 = board.get_potential_noncapture_sequences_for_man(piece)
        #self.assertListEqual(moves, [(4,1)])

    def test_get_possible_captures_for_man_from_field(self):
        board = Board()
        possible_sequences = board.get_potential_capture_sequences_for_man(board.board[3][2], 3, 2)
        self.assertListEqual(possible_sequences, [])

        board.board[4][3] = Piece(4,3,Player.PLAYER_BOTTOM)
        possible_sequences = board.get_potential_capture_sequences_for_man(board.board[3][2], 3, 2)
        self.assertEqual(possible_sequences[0].sequence[0], Move(3, 2, 5, 4, captured_piece = board.board[4][3]))

        board.board[6][1] = 0
        board.board[7][2] = 0
        board.board[7][4] = 0
        board.board[7][6] = 0
        possible_sequences = board.get_potential_capture_sequences_for_man(board.board[3][2], 3, 2)
        self.assertEqual(len(possible_sequences), 2)
        # self.assertListEqual(moves, [])
        # game.board.board[4][3] = Piece(4, 3, Player.PLAYER_BOTTOM)
        # game.board.board[4][5] = Piece(4, 5, Player.PLAYER_BOTTOM)
        # game.board.board[6][1] = 0
        # game.board.board[7][2] = 0
        # game.board.board[7][4] = 0
        # game.board.board[7][6] = 0



    def t_get_possible_captures_for_king(self):
        board = Board()
        # for row in range(ROWS):
        #     for col in range(COLUMNS):
        #         game.board.board[row][col] = 0
        #
        # game.board.board[0][3] = Piece(0, 3, Player.PLAYER_TOP)
        # game.board.board[0][3].promote_piece()
        # game.board.board[2][5] = Piece(2, 5, Player.PLAYER_BOTTOM)
        # game.board.board[4][5] = Piece(4, 5, Player.PLAYER_BOTTOM)
        # game.board.board[4][3] = Piece(4, 3, Player.PLAYER_BOTTOM)
        # game.board.board[6][5] = Piece(6, 5, Player.PLAYER_BOTTOM)
        # game.board.board[5][8] = Piece(5, 8, Player.PLAYER_BOTTOM)

    def t_get_possible_noncapture_moves_for_king(self):
        board = Board()
        # for row in range(ROWS):
        #     for col in range(COLUMNS):
        #         game.board.board[row][col] = 0
        # game.board.board[6][5] = Piece(6, 5, Player.PLAYER_TOP)
        # game.board.board[6][5].promote_piece()

if __name__ == "__main__":
    unittest.main()