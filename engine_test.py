from engine import Chess, PieceTeam, PieceName
import unittest

class TestChessClassFunctions(unittest.TestCase):
    def test_get_piece_normal_board_layout(self):
        C = Chess()

        # Rook
        expected = (PieceName.ROOK, PieceTeam.BLACK)
        actual = C.get_piece(0, 0)

        self.assertEqual(expected, actual)

        # Knight
        expected = (PieceName.KNIGHT, PieceTeam.WHITE)
        actual = C.get_piece(1, 7)

        self.assertEqual(expected, actual)

        # None
        expected = None
        actual = C.get_piece(3, 3)

        self.assertEqual(expected, actual)

    def test_get_piece_out_of_board(self):
        self.assertFalse(Chess().get_piece(10, 10))


class TestPieceMovement(unittest.TestCase):
    def test_pawn_moves(self):
        pass

if __name__ == '__main__':
    unittest.main()
