import unittest
from checkers.Player import Player
from checkers.Piece import Piece
from checkers.Board import Board
from checkers.Move import Move
from checkers.game_constants import ROWS, COLUMNS


class TestBoard(unittest.TestCase):
    def test_get_piece(self):
        board = Board()
        self.assertEqual(board.get_piece(0, 0), -1)
        self.assertIsInstance(board.get_piece(0, 1), Piece)
        self.assertEqual(board.get_piece(4, 1), 0)

    def test__is_out_of_bound(self):
        board = Board()
        self.assertTrue(board.is_out_of_bound(-1, 0))
        self.assertTrue(board.is_out_of_bound(5, -1))
        self.assertTrue(board.is_out_of_bound(ROWS, 0))
        self.assertTrue(board.is_out_of_bound(9, COLUMNS))
        self.assertFalse(board.is_out_of_bound(9, 9))

    def test_get_possible_noncapture_moves_for_man(self):
        board = Board()
        piece = board.get_piece(0, 1)
        moves = board._get_potential_non_capture_sequences_for_man(piece)
        self.assertListEqual(moves, [])

    def test_get_possible_captures_for_man_from_field(self):
        board = Board()
        possible_sequences = board._get_potential_capture_sequences_for_man(board.board[3][2], 3, 2)
        self.assertListEqual(possible_sequences, [])

        board.board[4][3] = Piece(4,3,Player.PLAYER_BOTTOM)
        possible_sequences = board._get_potential_capture_sequences_for_man(board.board[3][2], 3, 2)
        self.assertEqual(possible_sequences[0].sequence[0], Move(3, 2, 5, 4, captured_piece=board.board[4][3]))

        board.board[6][1] = 0
        board.board[7][2] = 0
        board.board[7][4] = 0
        board.board[7][6] = 0
        possible_sequences = board._get_potential_capture_sequences_for_man(board.board[3][2], 3, 2)
        self.assertEqual(len(possible_sequences), 2)


if __name__ == "__main__":
    unittest.main()