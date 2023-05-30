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
        moves = board.get_possible_noncapture_moves_for_man(piece)
        self.assertListEqual(moves, [])

        piece2 = board.get_piece(3, 0)
        moves2 = board.get_possible_noncapture_moves_for_man(piece)
        #self.assertListEqual(moves, [(4,1)])

    def test_get_possible_captures_for_man_from_field(self):
        board = Board()
        moves = board.get_possible_captures_for_man_from_field(board.board[3][2], 3, 2)
        self.assertListEqual(moves, [])

        piece_to_capture = Piece(4,3,Player.PLAYER_BOTTOM)
        board.board[4][3] = piece_to_capture
        moves = board.get_possible_captures_for_man_from_field(board.board[3][2], 3, 2)
        self.assertEqual(moves[0][0], Move(3, 2, 5, 4, captured_piece = piece_to_capture))

        board.board[6][1] = 0
        board.board[7][2] = 0
        board.board[7][4] = 0
        board.board[7][6] = 0
        moves = board.get_possible_captures_for_man_from_field(board.board[3][2], 3, 2)
        print(moves)
        # self.assertListEqual(moves, [])
        #

if __name__ == "__main__":
    unittest.main()