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


class TestRookMovement(unittest.TestCase):

    def test_rook_movement_init_pos(self):
        C = Chess()

        self.assertEqual([], C.r(0, 0))
        self.assertEqual([], C.r(7, 0))
        self.assertEqual([], C.r(7, 0))
        self.assertEqual([], C.r(7, 7))

    def test_rook_in_corner_with_no_other_pieces(self):
        C = Chess()
        C.board = (
            'r.......',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
        )

        expected = ([(i, 0) for i in range(1, 8)] +
                    [(0, i) for i in range(1, 8)])
        actual = C.r(0, 0)

        self.assertEqual(expected, actual)

    def test_rook_movement_in_middle_of_board_with_no_other_pieces(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '...R....',
            '........',
            '........',
            '........',
        )

        expected = ([(i, 4)
                     for a in [(4, 8, 1), (2, -1, -1)]
                     for i in range(a[0], a[1], a[2])] +
                    [(3, i)
                     for a in [(5, 8, 1), (3, -1, -1)]
                     for i in range(a[0], a[1], a[2])])
        actual = C.r(3, 4)

        self.assertEqual(expected, actual)


class TestKnightMovement(unittest.TestCase):

    def test_knight_init_pos(self):
        C = Chess()

        expected = [(2, 2), (0, 2)]
        actual = C.n(1, 0)

        self.assertEqual(expected, actual)

        expected = [(7, 5), (5, 5)]
        actual = C.n(6, 7)

        self.assertEqual(expected, actual)

    def test_knight_movement_free_board(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '....n...',
            '........',
            '........',
            '........',
        )

        expected = [(4 + x, 4 + y)
                    for x, y in [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1),
                                 (2, -1), (-2, 1), (-2, -1)]]
        actual = C.n(4, 4)

        self.assertEqual(expected, actual)

    def test_knight_attacking_moves(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '...p.P..',
            '..p...p.',
            '....n...',
            '..p...p.',
            '...p.p..',
            '........',
        )

        expected = [(5, 2)]
        actual = C.n(4, 4)

        self.assertEqual(expected, actual)


class TestBishopMovement(unittest.TestCase):
    def test_bishop_init_pos(self):
        C = Chess()

        self.assertEqual([], C.b(2, 0))
        self.assertEqual([], C.b(5, 0))
        self.assertEqual([], C.b(2, 7))
        self.assertEqual([], C.b(5, 7))

    def test_bishop_free_board(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '....b...',
            '........',
            '........',
            '........',
        )

        expected = (
            [(4 + i, 4 + i) for i in range(1, 4)] +
            [(4 + i, 4 - i) for i in range(1, 4)] +
            [(4 - i, 4 + i) for i in range(1, 4)] +
            [(4 - i, 4 - i) for i in range(1, 5)]
        )
        actual = C.b(4, 4)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
