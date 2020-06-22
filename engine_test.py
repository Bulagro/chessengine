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


class TestPawnMovement(unittest.TestCase):
    def test_pawn_moves_starting_position(self):
        C = Chess()

        for i in range(8):
            # Black
            expected = [(i, 2), (i, 3)]
            actual = C.p(i, 1)

            self.assertEqual(expected, actual)

            # White
            expected = [(i, 5), (i, 4)]
            actual = C.p(i, 6)

            self.assertEqual(expected, actual)

    def test_pawn_attack_moves(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '..pPp...',
            '...P....',
            '........',
            '........',
            '........',
        )

        expected = [(4, 3), (2, 3)]
        actual = C.p(3, 4)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
