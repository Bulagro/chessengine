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

        expected = (None, None)
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
            [(4 + i, 4 + j) for i, j in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]]
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

    def test_get_piece_moves_pawn_considering_pins(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '...p....',
            '..R.....',
            '........',
            '........',
            '........',
        )
        C.pinned_pieces = {
            (3, 3) : [(2, 4)]
        }

        expected = [(2, 4)]
        actual = C.get_piece_moves(3, 3, consider_pins=True)

        self.assertEqual(expected, actual)

    def test_get_piece_moves_knight_considering_pins(self):
        C = Chess()
        C.board = (
            'n.......',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
        )
        C.pinned_pieces = {
            (0, 0) : [(2, 1)]
        }

        expected = [(2, 1)]
        actual = C.get_piece_moves(0, 0, consider_pins=True)

        self.assertEqual(expected, actual)

    def test_get_piece_moves_rook_considering_pins(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '...r....',
            '........',
            '........',
            '........',
            '........',
        )
        C.pinned_pieces = {
            (3, 3) : [(4, 3), (5, 3), (6, 3), (7, 3), (2, 3), (1, 3), (0, 3)]
        }

        expected = [(4, 3), (5, 3), (6, 3), (7, 3), (2, 3), (1, 3), (0, 3)]
        actual = C.get_piece_moves(3, 3, consider_pins=True)

        self.assertEqual(expected, actual)

    def test_find_king_pos(self):
        C = Chess()

        self.assertEqual((4, 0), C.find_king_pos(PieceTeam.BLACK))

    def test_can_move_default_board(self):
        C = Chess()

        self.assertTrue(C.can_move(PieceTeam.BLACK))
        self.assertTrue(C.can_move(PieceTeam.WHITE))

    def test_can_move_when_on_check_and_avaliable_moves(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '....R...',
            '........',
            '...n....',
            '........',
            '....k...',
        )

        C.get_king_status(PieceTeam.BLACK)
        self.assertTrue(C.can_move(PieceTeam.BLACK))

    def test_can_move_with_no_avaliable_moves(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            'p.......',
            'P.......',
            '........',
            '........',
            '........',
        )

        self.assertFalse(C.can_move(PieceTeam.WHITE))
        self.assertFalse(C.can_move(PieceTeam.BLACK))

    def test_can_move_draw(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '.r......',
            '.....k.K',
        )

        self.assertFalse(C.can_move(PieceTeam.WHITE))
        self.assertEqual(None, C.in_check)
        self.assertEqual(None, C.checkmate)

    def test_move_piece_piece_forward(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '...p....',
            '........',
            '........',
            '........',
            '........',
        )

        C.move_piece(3, 3, 3, 4, False)

        self.assertEqual('........', C.board[3])
        self.assertEqual('...p....', C.board[4])

    def test_move_piece_attack(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '...p....',
            '..P.....',
            '........',
            '........',
            '........',
        )
        C.move_piece(3, 3, 2, 4, False)

        self.assertEqual('........', C.board[3])
        self.assertEqual('..p.....', C.board[4])

    def test_move_piece_castle(self):
        C = Chess()
        C.board = (
            'r...k...',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '....K..R',
        )
        C.move_piece(4, 0, 0, 0, True)
        C.move_piece(4, 7, 7, 7, True)

        self.assertEqual('..kr....', C.board[0])
        self.assertEqual('.....RK.', C.board[7])

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

    def test_rook_attacking_moves(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '...p....',
            '........',
            'p..R.p..',
            '........',
            '........',
            '...p....',
        )

        expected = [
            (4, 4), (5, 4),         # Right
            (2, 4), (1, 4), (0, 4), # Left
            (3, 5), (3, 6), (3, 7), # Down
            (3, 3), (3, 2)          # Up
        ]

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
        C.has_king_moved = [True, True]
        C.has_rook_moved = [[True, True], [True, True]]

        expected = (
            [(4 + i, 4 + j) for i, j in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]]
        )
        actual = C.k(4, 4)

        self.assertEqual(expected, actual)

    def test_every_square_the_king_cant_be_in_default_board(self):
        C = Chess()

        expected = set(
            [(i, 5) for i in range(8)] +                       # Pawn attacks
            [(0, 6), (1, 7), (7, 6), (6, 7)] +                 # Pieces defended by rooks
            [(3, 6), (0, 5), (2, 5), (4, 6), (5, 5), (7, 5)] + # Squares defended by knights
            [(1, 6), (3, 6), (4, 6), (6, 6)] +                 # Pieces defended by bishops
            [(2, 7), (2, 6), (3, 6), (4, 6)] +                 # Pieces defended by queen
            [(3, 7), (3, 6), (4, 6), (5, 6), (5, 7)]           # Pieces defended by the king.
        )
        actual = set(C.get_every_square_the_king_cant_be_in(PieceTeam.BLACK))

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

    def test_restricted_king_movement_straight_line(self):
        C = Chess()
        C.board = (
            '.....R..',
            '........',
            '........',
            '....k...', # 4, 3
            '........',
            '........',
            '........',
            '........',
        )
        C.has_king_moved = [True, True]
        C.has_rook_moved = [[True, True], [True, True]]

        expected = [(4, 4), (3, 4), (3, 3), (3, 2), (4, 2)]
        actual = C.get_piece_moves(4, 3)

        self.assertEqual(expected, actual)

    def test_restricted_king_movement_straight_line_more_restrictions(self):
        C = Chess()
        C.board = (
            '.....R..',
            '........',
            '........',
            '....k...', # 4, 3
            'R.......',
            '........',
            '........',
            '........',
        )
        C.has_king_moved = [True, True]
        C.has_rook_moved = [[True, True], [True, True]]

        expected = [(3, 3), (3, 2), (4, 2)]
        actual = C.get_piece_moves(4, 3)

        self.assertEqual(expected, actual)

    def test_king_cant_go_in_the_same_line_as_his_threatener(self):
        C = Chess()
        C.board = (
            '.K...r..',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
        )
        C.has_king_moved = [True, True]
        C.has_rook_moved = [[True, True], [True, True]]

        expected = [(2, 1), (1, 1), (0, 1)]
        actual = C.get_piece_moves(1, 0)

        self.assertEqual(expected, actual)

        C.board = (
            '........',
            '.K......',
            '..b.....',
            '........',
            '........',
            '........',
            '........',
            '........',
        )

        expected = [(2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (1, 0), (2, 0)]
        actual = C.get_piece_moves(1, 1)

        self.assertEqual(expected, actual)

    def test_restricted_king_movement_diagonal_line(self):
        C = Chess()
        C.board = (
            '..B.....',
            '........',
            '........',
            '....k...', # 4, 3
            '........',
            '........',
            '........',
            '........',
        )
        C.has_king_moved = [True, True]
        C.has_rook_moved = [[True, True], [True, True]]

        expected = [(5, 4), (4, 4), (3, 4), (3, 3), (3, 2), (5, 2)]
        actual = C.get_piece_moves(4, 3, False)

        self.assertEqual(expected, actual)

    def test_restricted_king_movement_diagonal_line_more_restrictions(self):
        C = Chess()
        C.board = (
            '..B.....',
            '........',
            '........',
            '....k...', # 4, 3
            '........',
            '........',
            '..B.....',
            '........',
        )
        C.has_king_moved = [True, True]
        C.has_rook_moved = [[True, True], [True, True]]

        expected = [(5, 4), (3, 4), (3, 3), (3, 2), (5, 2)]
        actual = C.get_piece_moves(4, 3, False)

        self.assertEqual(expected, actual)

    def test_restricted_king_movement_by_knight(self):
        C = Chess()
        C.board = (
            '....n...',
            '........',
            '........',
            '....K...', # 4, 3
            '........',
            '....n...',
            '........',
            '........',
        )

        expected = [(5, 4), (4, 4), (3, 4), (4, 2)]
        actual = C.get_piece_moves(4, 3, False)

        self.assertEqual(expected, actual)

    def test_restricted_king_movement_by_pawn(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '....k...', # 4, 3
            '....P...',
            '........',
            '........',
            '........',
        )
        C.has_king_moved = [True, True]
        C.has_rook_moved = [[True, True], [True, True]]

        expected = [(5, 4), (4, 4), (3, 4), (3, 2), (4, 2), (5, 2)]
        actual = C.get_piece_moves(4, 3, False)

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

        for team in (PieceTeam.WHITE, PieceTeam.BLACK):
            C.get_king_status(team)

            self.assertIsNone(C.in_check)
            self.assertEqual(C.moves_to_defend_check, [])
            self.assertEqual(C.pinned_pieces, {})

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

        C.get_king_status(PieceTeam.WHITE)

        self.assertIsNone(C.in_check)
        self.assertEqual(C.pinned_pieces, {})
        self.assertEqual(C.moves_to_defend_check, [])

    def test_get_king_status_one_pinned_pawn_straight_line(self):
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

        C.get_king_status(PieceTeam.WHITE)
        expected = {
            (5, 7) : []
        }

        self.assertIsNone(C.in_check)
        self.assertEqual(expected, C.pinned_pieces)
        self.assertEqual(C.moves_to_defend_check, [])

    def test_get_king_status_one_pinned_rook_straight_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '.K...R.r',
        )

        C.get_king_status(PieceTeam.WHITE)
        expected = {
            (5, 7) : [(6, 7), (7, 7), (4, 7), (3, 7), (2, 7)]
        }

        self.assertIsNone(C.in_check)
        self.assertEqual(expected, C.pinned_pieces)
        self.assertEqual(C.moves_to_defend_check, [])

    def test_get_king_status_one_pinned_piece_and_check_straight_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '.q......',
            '........',
            '........',
            '.K...R.r',
        )

        C.get_king_status(PieceTeam.WHITE)
        expected_check = PieceTeam.WHITE
        expected_pins = {
            (5, 7) : [(6, 7), (7, 7), (4, 7), (3, 7), (2, 7)]
        }
        expected_moves_to_defend_check = [
            (1, 6), (1, 5), (1, 4)
        ]

        self.assertEqual(expected_check, C.in_check)
        self.assertEqual(expected_pins, C.pinned_pieces)
        self.assertEqual(expected_moves_to_defend_check, C.moves_to_defend_check)

    def test_get_king_status_multiple_pinned_pieces_straight_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '.q......',
            '.P......',
            '........',
            '.K...R.r',
        )

        C.get_king_status(PieceTeam.WHITE)
        expected_pins = {
            (5, 7) : [(6, 7), (7, 7), (4, 7), (3, 7), (2, 7)],
            (1, 5) : [],
        }

        self.assertIsNone(C.in_check)
        self.assertEqual(expected_pins, C.pinned_pieces)
        self.assertEqual(C.moves_to_defend_check, [])

    def test_get_king_status_one_non_pinned_piece_since_the_attacker_cant_attack_in_that_direction(self):
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

        C.get_king_status(PieceTeam.WHITE)

        self.assertIsNone(C.in_check)
        self.assertEqual(C.pinned_pieces, {})
        self.assertEqual(C.moves_to_defend_check, [])

    def test_get_king_status_not_pinning_same_team_piece_straight_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '.r......',
            '.b......',
            '........',
            '.K......',
        )

        C.get_king_status(PieceTeam.WHITE)

        self.assertIsNone(C.in_check)
        self.assertEqual(C.pinned_pieces, {})
        self.assertEqual(C.moves_to_defend_check, [])

    def test_get_king_status_one_pinned_pawn_diagonal_line(self):
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

        C.get_king_status(PieceTeam.WHITE)
        expected_pin = {
            (2, 6) : []
            }

        self.assertIsNone(C.in_check)
        self.assertEqual(expected_pin, C.pinned_pieces)
        self.assertEqual(C.moves_to_defend_check, [])

    def test_get_king_status_one_pinned_queen_diagonal_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '....b...',
            '........',
            '..Q.....',
            '.K......',
        )

        C.get_king_status(PieceTeam.WHITE)
        expected_pin = {
            (2, 6) : [(3, 5), (4, 4)]
            }

        self.assertIsNone(C.in_check)
        self.assertEqual(expected_pin, C.pinned_pieces)
        self.assertEqual(C.moves_to_defend_check, [])

    def test_get_king_status_multiple_pinned_pieces_diagonal_line(self):
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

        C.get_king_status(PieceTeam.BLACK)
        expected_pins = {
            (4, 6) : [(5, 7)],
            (5, 3) : [],
        }

        self.assertIsNone(C.in_check)
        self.assertEqual(expected_pins, C.pinned_pieces)
        self.assertEqual(C.moves_to_defend_check, [])

    def test_get_king_status_not_pinning_same_team_piece_diagonal_line(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '....B...',
            '........',
            '..P.....',
            '.k......',
        )

        C.get_king_status(PieceTeam.BLACK)

        self.assertIsNone(C.in_check)
        self.assertEqual(C.pinned_pieces, {})
        self.assertEqual(C.moves_to_defend_check, [])

    def test_get_king_status_check_diagonal_line(self):
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

        C.get_king_status(PieceTeam.BLACK)
        expected_moves_to_defend_check = [(2, 6), (3, 5)]

        self.assertEqual(PieceTeam.BLACK, C.in_check)
        self.assertEqual(C.pinned_pieces, {})
        self.assertEqual(expected_moves_to_defend_check, C.moves_to_defend_check)

    def test_get_king_status_pinned_pieces_and_check_diagonal_line(self):
        C = Chess()
        C.board = (
            '........',
            'b.......',
            '........',
            '..P.....',
            '...K....',
            '........',
            '.q......',
            '........',
        )

        C.get_king_status(PieceTeam.WHITE)
        expected_pin = {
            (2, 3) : []
        }
        expected_moves_to_defend_check = [(2, 5), (1, 6)]

        self.assertEqual(PieceTeam.WHITE, C.in_check)
        self.assertEqual(expected_pin, C.pinned_pieces)
        self.assertEqual(expected_moves_to_defend_check, C.moves_to_defend_check)

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

        C.get_king_status(PieceTeam.BLACK)
        expected_moves_to_defend_check = [(3, 5)]

        self.assertEqual(PieceTeam.BLACK, C.in_check)
        self.assertEqual(C.pinned_pieces, {})
        self.assertEqual(expected_moves_to_defend_check, C.moves_to_defend_check)

        C.board = (
            '........',
            '........',
            '........',
            '........',
            '....k...',
            '.....P..',
            '........',
            '........',
        )

        C.get_king_status(PieceTeam.BLACK)
        expected_moves_to_defend_check = [(5, 5)]

        self.assertEqual(PieceTeam.BLACK, C.in_check)
        self.assertEqual(C.pinned_pieces, {})
        self.assertEqual(expected_moves_to_defend_check, C.moves_to_defend_check)

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

        C.get_king_status(PieceTeam.BLACK)
        expected_moves_to_defend_check = [(3, 6)]

        self.assertEqual(C.in_check, PieceTeam.BLACK)
        self.assertEqual(C.pinned_pieces, {})
        self.assertEqual(expected_moves_to_defend_check, C.moves_to_defend_check)

    def test_limited_piece_movement_when_in_check(self):
        C = Chess()
        C.board = (
            '........',
            '...p....',
            '....R...',
            '........',
            '....k...',
            '.b......',
            '........',
            '........',
        )

        C.get_king_status(PieceTeam.BLACK)

        self.assertEqual(PieceTeam.BLACK, C.in_check)
        self.assertEqual( # Pawn
            [(4, 2)],
            C.get_piece_moves(3, 1)
        )
        self.assertEqual(
            [(4, 2)],
            C.get_piece_moves(1, 5)
        )

    def test_king_can_castle_with_both_rooks_perfect_conditions(self):
        C = Chess()
        C.board = (
            'r...k..r',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            'R...K..R',
        )

        self.assertTrue((0, 0) and (7, 0) in C.get_piece_moves(4, 0))
        self.assertTrue((0, 7) and (7, 7) in C.get_piece_moves(4, 7))

    def test_king_cant_castle_with_pice_in_between(self):
        C = Chess()
        C.board = (
            'r.n.k..r',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            'R...K..R',
        )

        self.assertEqual(
            [(5, 0), (5, 1), (4, 1), (3, 1), (3, 0), (7, 0)],
            C.get_piece_moves(4, 0)
        )
        self.assertTrue((0, 7) and (7, 7) in C.get_piece_moves(4, 7))

    def test_king_cant_castle_with_oposing_piece_threatening_square(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '..r.....',
            '........',
            '........',
            'R...K..R',
        )

        self.assertTrue((0, 0) not in C.get_piece_moves(4, 7))

    def test_king_cant_castle_already_moved_rook(self):
        C = Chess()
        C.board = (
            'r...k..r',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
        )
        C.has_rook_moved = [[False, False], [True, False]]

        self.assertTrue((0, 0) not in C.get_piece_moves(4, 0))


class TestCheckmate(unittest.TestCase):
    def test_checkmate_with_rooks(self):
        C = Chess()
        C.board = (
            '......RR',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '.......k',
        )

        C.get_king_status(PieceTeam.BLACK)

        self.assertEqual(PieceTeam.BLACK, C.in_check)
        self.assertEqual(PieceTeam.BLACK, C.checkmate)
        self.assertEqual({}, C.pinned_pieces)
        self.assertEqual(
            [(7, i) for i in range(6, -1, -1)],
            C.moves_to_defend_check
            )

    def test_checkmate_with_knight(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '......QR',
            '........',
            '........',
            'R....N.P',
            '.......k',
        )

        C.get_king_status(PieceTeam.BLACK)

        self.assertEqual(PieceTeam.BLACK, C.in_check)
        self.assertEqual(PieceTeam.BLACK, C.checkmate)
        self.assertEqual({}, C.pinned_pieces)
        self.assertEqual([(5, 6)], C.moves_to_defend_check)

    def test_checkmate_with_pawn(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '.....b..',
            '........',
            '...pBB..',
            '...PKR..',
        )

        C.get_king_status(PieceTeam.WHITE)

        self.assertEqual(PieceTeam.WHITE, C.in_check)
        self.assertEqual(PieceTeam.WHITE, C.checkmate)
        self.assertEqual({}, C.pinned_pieces)
        self.assertEqual([(3, 6)], C.moves_to_defend_check)
        self.assertEqual([], C.get_piece_moves(4, 7))

    def test_not_checkmate_with_possible_move(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '...p....',
            '...PKR..',
        )

        C.get_king_status(PieceTeam.WHITE)

        self.assertTrue(C.can_move(PieceTeam.WHITE))
        self.assertEqual(PieceTeam.WHITE, C.in_check)
        self.assertEqual(None, C.checkmate)
        self.assertEqual({}, C.pinned_pieces)
        self.assertEqual([(3, 6)], C.moves_to_defend_check)


class TestsForBugs(unittest.TestCase):
    def test_pieces_duplicate_on_horizontal_movement(self):
        C = Chess()
        C.board = (
            '........',
            '........',
            '........',
            '........',
            '...k....',
            '........',
            '........',
            '........',
        )

        C.move_piece(3, 4, 2, 4, False)

        self.assertEqual(C.board[4], '..k.....')

if __name__ == '__main__':
    unittest.main()
