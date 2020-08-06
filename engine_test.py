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

    def test_get_piece_moves_default_board(self):
        C = Chess()

        self.assertEqual(
            C.get_piece_moves(0, 0),
            C.r(0, 0)
        )

        self.assertEqual(
            C.get_piece_moves(1, 0),
            C.n(1, 0)
        )

    def test_get_piece_moves_pawn_with_protected_pieces(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '..p.....',
            '.n.r....',
            '........',
            '........',
            '........',
        )

        expected = [(2, 4), (3, 4), (1, 4)]
        actual = C.get_piece_moves(2, 3, True)

        self.assertEqual(expected, actual)

    def test_get_piece_moves_rook_with_protected_pieces(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '..p.....',
            '.prp....',
            '..p.....',
            '........',
            '........',
            '........',
        )

        expected = [(3, 3), (1, 3), (2, 4), (2, 2)]
        actual = C.get_piece_moves(2, 3, True)

        self.assertEqual(expected, actual)

    def test_get_piece_moves_bishop_with_protected_pieces(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '.r.r....',
            '..b.....',
            '.r.r....',
            '........',
            '........',
            '........',
        )

        expected = [(3, 4), (3, 2), (1, 4), (1, 2)]
        actual = C.get_piece_moves(2, 3, True)

        self.assertEqual(expected, actual)

    def test_get_piece_moves_knight_with_protected_pieces(self):
        C = Chess()
        C.board = (
            'n.......',
            '..p.....',
            '.p......',
            '........',
            '........',
            '........',
            '........',
            '........',
        )

        expected = [(1, 2), (2, 1)]
        actual = C.get_piece_moves(0, 0, True)

        self.assertEqual(expected, actual)

    def test_get_piece_moves_king_with_protected_pieces(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '...ppp..',
            '...pkp..',
            '...ppp..',
            '........',
            '........',
        )

        expected = (
            [(4 + i, 4 + j) for i, j in [(1, 0), (1, 1), (0, 1), (1, -1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]]
        )
        actual = C.get_piece_moves(4, 4, True)

        self.assertEqual(expected, actual)

    def test_get_piece_moves_with_protected_pieces_ignores_king(self):
        C = Chess()
        C.board = (
            'n.......',
            '..k.....',
            '.p......',
            '........',
            '........',
            '........',
            '........',
            '........',
        )

        expected = [(1, 2)]
        actual = C.get_piece_moves(0, 0, True)

        self.assertEqual(expected, actual)

    def test_find_king_pos(self):
        C = Chess()

        self.assertEqual(
            (4, 0),
            C.find_king_pos(PieceTeam.BLACK)
        )

    def test_every_square_the_king_cant_be_in_default_board(self):
        C = Chess()

        expected = [
            # Ffffffffff
        ]
        actual = C.get_every_square_the_king_cant_be_in(PieceTeam.BLACK)

        self.assertEqual(expected, actual)

    def test_every_square_the_king_cant_be_in_empty_board(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '....k...',
            '........',
            '........',
            '........',
        )

        expected = []
        actual = C.get_every_square_the_king_cant_be_in(PieceTeam.BLACK)

        self.assertEqual(expected, actual)

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

    def test_pawn_cant_eat_king(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '..k.k...',
            '...P....',
            '........',
            '........',
            '........',
        )

        expected = [(3, 3)]
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

    def test_rook_cant_eat_king(self):
        C = Chess()
        C.board = (
            'R..k....',
            '........',
            'K.......',
            '........',
            '........',
            '........',
            '........',
            '........',
        )

        expected = [(1, 0), (2, 0), (0, 1)]
        actual = C.r(0, 0)

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

    def test_knight_cant_eat_king(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '...p.P..',
            '..K...p.',
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

    def test_bishop_attacking_moves(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '......P.',
            '...P....',
            '....b...',
            '...P.P..',
            '........',
            '........',
        )

        expected = [(5, 5), (5, 3), (6, 2), (3, 5), (3, 3)]
        actual = C.b(4, 4)

        self.assertEqual(expected, actual)

    def test_bishop_cant_eat_king(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '......P.',
            '...K....',
            '....b...',
            '...P.P..',
            '........',
            '........',
        )

        expected = [(5, 5), (5, 3), (6, 2), (3, 5)]
        actual = C.b(4, 4)

        self.assertEqual(expected, actual)


class TestQueenMovement(unittest.TestCase):
    def test_queen_init_pos(self):
        C = Chess()

        self.assertEqual([], C.q(3, 0))
        self.assertEqual([], C.q(3, 7))

    def test_queen_empty_board(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '....q...',
            '........',
            '........',
            '........',
        )

        expected_straight = ( # Straight
            [(4 + i, 4) for i in range(1, 4)] +
            [(4 - i, 4) for i in range(1, 5)] +
            [(4, 4 + i) for i in range(1, 4)] +
            [(4, 4 - i) for i in range(1, 5)]
        )

        expected_diagonal = ( # Diagonal
            [(4 + i, 4 + i) for i in range(1, 4)] +
            [(4 + i, 4 - i) for i in range(1, 4)] +
            [(4 - i, 4 + i) for i in range(1, 4)] +
            [(4 - i, 4 - i) for i in range(1, 5)]
        )

        self.assertEqual(
            expected_straight + expected_diagonal,
            C.q(4, 4)
        )

    def queen_cant_eat_king(self):
        C = Chess()
        C.board = (
            'q..K....',
            'p.......',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
        )

        expected = [(1, 0), (2, 0)]
        actual = C.q(0, 0)

        self.assertEqual(expected, actual)


class TestKingMovement(unittest.TestCase):
    def test_king_movement_init_pos(self):
        C = Chess()

        self.assertEqual([], C.k(4, 0))

    def test_king_movement_empty_board(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '....k...',
            '........',
            '........',
            '........',
        )

        expected = (
            [(4 + i, 4 + j) for i, j in [(1, 0), (1, 1), (0, 1), (1, -1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]]
        )
        actual = C.k(4, 4)

        self.assertEqual(expected, actual)

    def test_get_king_status_on_empty_board_with_only_two_non_interfiering_kings(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '.....K..',
            '........',
            '........',
            '...k....',
            '........',
            '........',
        )

        expected_w = []
        C.in_check, actual_w = C.get_king_status(PieceTeam.WHITE)

        self.assertEqual(expected_w, actual_w)
        self.assertEqual(None, C.in_check)

        expected_b = []
        C.in_check, actual_b = C.get_king_status(PieceTeam.BLACK)

        self.assertEqual(expected_b, actual_b)
        self.assertEqual(None, C.in_check)

    def test_get_king_status_no_pinned_pieces_straight_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '.K.P.P.r',
        )

        expected = []
        C.in_check, actual = C.get_king_status(PieceTeam.WHITE)

        self.assertEqual(expected, actual)
        self.assertEqual(None, C.in_check)

    def test_get_king_status_one_pinned_piece_straight_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '.K...P.r',
        )

        expected = [(5, 7)]
        C.in_check, actual = C.get_king_status(PieceTeam.WHITE)

        self.assertEqual(expected, actual)
        self.assertEqual(None, C.in_check)

    def test_king_status_one_non_pinned_piece_since_the_attacker_cant_attack_in_that_direction(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '.b......',
            '.N......',
            '........',
            '.K......',
        )

        expected = []
        C.in_check, actual = C.get_king_status(PieceTeam.WHITE)

        self.assertEqual(expected, actual)
        self.assertEqual(None, C.in_check)

    def test_get_king_status_multiple_pinned_pieces_straight_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '.q......',
            '.N......',
            '........',
            '.K...P.r',
        )

        expected = [(5, 7), (1, 5)]
        C.in_check, actual = C.get_king_status(PieceTeam.WHITE)

        self.assertEqual(expected, actual)
        self.assertEqual(None, C.in_check)

    def test_king_status_one_pinned_piece_diagonal_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '....b...',
            '........',
            '..P.....',
            '.K......',
        )

        expected = [(2, 6)]
        C.in_check, actual = C.get_king_status(PieceTeam.WHITE)

        self.assertEqual(expected, actual)
        self.assertEqual(None, C.in_check)

    def test_king_status_multiple_pinned_pieces_diagonal_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '......B.',
            '.....r..',
            '........',
            '...k....',
            '....p...',
            '.....B..',
        )

        expected = [(4, 6), (5, 3)]
        C.in_check, actual = C.get_king_status(PieceTeam.BLACK)

        self.assertEqual(expected, actual)
        self.assertEqual(None, C.in_check)

    def test_king_status_check_straight_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '.k.....Q',
        )

        expected = [(2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]
        C.in_check, actual = C.get_king_status(PieceTeam.BLACK)

        self.assertEqual(expected, actual)
        self.assertEqual(C.in_check, PieceTeam.BLACK)

    def test_king_status_check_diagonal_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '........',
            '...B....',
            '........',
            '.k......',
        )

        expected = [(2, 6), (3, 5)]
        C.in_check, actual = C.get_king_status(PieceTeam.BLACK)

        self.assertEqual(expected, actual)
        self.assertEqual(C.in_check, PieceTeam.BLACK)

    def test_king_status_ignore_pinned_pieces_on_check(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '.r..b...',
            '.P......',
            '..N.....',
            '.K.....q',
        )

        expected = [(2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]
        C.in_check, actual = C.get_king_status(PieceTeam.WHITE)

        self.assertEqual(expected, actual)
        self.assertEqual(C.in_check, PieceTeam.WHITE)

    def test_king_status_not_pinning_other_teams_piece(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '.k.N...Q',
        )

        expected = []
        C.in_check, actual = C.get_king_status(PieceTeam.BLACK)

        self.assertEqual(expected, actual)
        self.assertEqual(None, C.in_check)

    def test_king_status_check_by_pawn(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '....k...',
            '...P....',
            '........',
            '........',
        )

        expected = [(3, 5)]
        C.in_check, actual = C.get_king_status(PieceTeam.BLACK)

        self.assertEqual(expected, actual)
        self.assertEqual(C.in_check, PieceTeam.BLACK)

        C.board = (
            '........',
            '........',
            '........',
            '.....p..',
            '....K...',
            '........',
            '........',
            '........',
        )

        expected = [(5, 3)]
        C.in_check, actual = C.get_king_status(PieceTeam.WHITE)

        self.assertEqual(expected, actual)
        self.assertEqual(C.in_check, PieceTeam.WHITE)

    def test_king_status_check_by_knight(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '....k...',
            '........',
            '...N....',
            '........',
        )

        expected = [(3, 6)]
        C.in_check, actual = C.get_king_status(PieceTeam.BLACK)

        self.assertEqual(expected, actual)
        self.assertEqual(C.in_check, PieceTeam.BLACK)


if __name__ == '__main__':
    unittest.main()
