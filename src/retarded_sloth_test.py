from engine import *
import unittest


class TestBoardEvaluation(unittest.TestCase):
    def test_equal_position_for_both_teams_result_in_equal_scores(self):
        C = Chess()
        R = RetardedSloth(C)

        white_score = R.evaluate_board(PieceTeam.WHITE, None)
        black_score = R.evaluate_board(PieceTeam.BLACK, None)
        self.assertEqual(white_score, black_score)

        C.board = (
            '..k.....',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '...K....',
        )

        white_score = R.evaluate_board(PieceTeam.WHITE, None)
        black_score = R.evaluate_board(PieceTeam.BLACK, None)
        self.assertEqual(white_score, black_score)

        C.board = (
            'k.......',
            '........',
            '.....p..',
            '........',
            '........',
            '.....P..',
            '........',
            '.......K',
        )

        white_score = R.evaluate_board(PieceTeam.WHITE, None)
        black_score = R.evaluate_board(PieceTeam.BLACK, None)
        self.assertEqual(white_score, black_score)

    def test_center_control_gives_more_points(self):
        C = Chess()
        R = RetardedSloth(C)

        C.board = (
            'k.......',
            '.....p..',
            '........',
            '........',
            '........',
            '...P....',
            '........',
            '........',
            '......K.',
        )

        white_score = R.evaluate_board(PieceTeam.WHITE, None)
        black_score = R.evaluate_board(PieceTeam.BLACK, None)

        self.assertTrue(white_score > black_score)

    def test_more_pieces_results_in_higher_score(self):
        C = Chess()
        R = RetardedSloth(C)

        C.board = (
            '..K.....',
            '........',
            '........',
            '...p....',
            '..k.....',
            '........',
            '...r....',
            '........',
        )

        white_score = R.evaluate_board(PieceTeam.WHITE, None)
        black_score = R.evaluate_board(PieceTeam.BLACK, None)

        self.assertTrue(white_score < black_score)


class TestTreeMovesGenerator(unittest.TestCase):
    def test_get_every_possible_board_with_only_one_possible_move(self):
        C = Chess()
        R = RetardedSloth(C)

        C.board = (
            '........',
            '..k.....',
            '........',
            '....r...',
            '........',
            '........',
            'r.......',
            '.....K..',
        )

        self.assertTrue(
            R.evaluate_board(PieceTeam.BLACK, None) > R.evaluate_board(PieceTeam.WHITE, None)
        )
        self.assertEqual(
            C.get_piece_moves(5, 7, consider_pins=True),
            [(6, 7)]
        )

        actual_board = R.get_every_possible_board(PieceTeam.WHITE)
        expected_board = [
            (
                ('........',
                '..k.....',
                '........',
                '....r...',
                '........',
                '........',
                'r.......',
                '......K.'),
                [(5, 7), (6, 7)],
                True, False, False, False, None,
            )
        ]

        self.assertEqual(expected_board, actual_board)

    def test_get_every_possible_board_with_more_than_one_square_for_the_king_to_move(self):
        C = Chess()
        R = RetardedSloth(C)

        C.board = (
            '........',
            '..k.....',
            '........',
            '...r....',
            '........',
            '........',
            'r.......',
            '.....K..',
        )

        actual_boards = R.get_every_possible_board(PieceTeam.WHITE)
        expected_boards = [
            (
                ('........',
                '..k.....',
                '........',
                '...r....',
                '........',
                '........',
                'r.......',
                '......K.'),
                [(5, 7), (6, 7)],
                True, False, False, False, None,
            ),
            (
                ('........',
                '..k.....',
                '........',
                '...r....',
                '........',
                '........',
                'r.......',
                '....K...'),
                [(5, 7), (4, 7)],
                True, False, False, False, None,
            )
        ]

        self.assertEqual(expected_boards, actual_boards)

    def test_only_20_moves_with_initial_board(self):
        C = Chess()
        R = RetardedSloth(C)

        self.assertEqual(
            len(R.get_every_possible_board(PieceTeam.WHITE)),
            20
        )

        self.assertEqual(
            len(R.get_every_possible_board(PieceTeam.BLACK)),
            20
        )

    def test_get_every_possible_board_registeres_lrook_and_king_movement(self):
        C = Chess()
        R = RetardedSloth(C)

        C.board = (
            '........',
            '.....k..',
            '........',
            '........',
            '........',
            '........',
            'P.......',
            'R..K....',
        )

        actual = R.get_every_possible_board(PieceTeam.WHITE)
        expected = [
            (
                ('........',
                '.....k..',
                '........',
                '........',
                '........',
                'P.......',
                '........',
                'R..K....'),
                [(0, 6), (0, 5)],
                False, False, False, False, None,
            ),
            (
                ('........',
                '.....k..',
                '........',
                '........',
                'P.......',
                '........',
                '........',
                'R..K....'),
                [(0, 6), (0, 4)],
                False, False, False, False, None,
            ),
            (
                ('........',
                '.....k..',
                '........',
                '........',
                '........',
                '........',
                'P.......',
                '.R.K....'),
                [(0, 7), (1, 7)],
                False, False, True, False, None,
            ),
            (
                ('........',
                '.....k..',
                '........',
                '........',
                '........',
                '........',
                'P.......',
                '..RK....'),
                [(0, 7), (2, 7)],
                False, False, True, False, None,
            ),
            (
                ('........',
                '.....k..',
                '........',
                '........',
                '........',
                '........',
                'P.......',
                'R...K...'),
                [(3, 7), (4, 7)],
                True, False, False, False, None,
            ),
            (
                ('........',
                '.....k..',
                '........',
                '........',
                '........',
                '........',
                'P.......',
                'R.K.....'),
                [(3, 7), (2, 7)],
                True, False, False, False, None,
            ),
            (
                ('........',
                '.....k..',
                '........',
                '........',
                '........',
                '........',
                'P.K.....',
                'R.......'),
                [(3, 7), (2, 6)],
                True, False, False, False, None,
            ),
            (
                ('........',
                '.....k..',
                '........',
                '........',
                '........',
                '........',
                'P..K....',
                'R.......'),
                [(3, 7), (3, 6)],
                True, False, False, False, None,
            ),
            (
                ('........',
                '.....k..',
                '........',
                '........',
                '........',
                '........',
                'P...K...',
                'R.......'),
                [(3, 7), (4, 6)],
                True, False, False, False, None,
            ),
        ]

        self.assertEqual(expected, actual)

    def test_get_every_move_registers_rrook_movement(self):
        C = Chess()
        R = RetardedSloth(C)

        C.board = (
            '....k...',
            '........',
            '........',
            '........',
            '........',
            '........',
            '.......P',
            '.....K.R',
        )

        actual = R.get_every_possible_board(PieceTeam.WHITE)
        expected = [
            (
                ('....k...',
                '........',
                '........',
                '........',
                '........',
                '.......P',
                '........',
                '.....K.R'),
                [(7, 6), (7, 5)],
                False, False, False, False, None,
            ),
            (
                ('....k...',
                '........',
                '........',
                '........',
                '.......P',
                '........',
                '........',
                '.....K.R'),
                [(7, 6), (7, 4)],
                False, False, False, False, None,
            ),
            (
                ('....k...',
                '........',
                '........',
                '........',
                '........',
                '........',
                '.......P',
                '......KR'),
                [(5, 7), (6, 7)],
                True, False, False, False, None
            ),
            (
                ('....k...',
                '........',
                '........',
                '........',
                '........',
                '........',
                '.......P',
                '....K..R'),
                [(5, 7), (4, 7)],
                True, False, False, False, None,
            ),
            (
                ('....k...',
                '........',
                '........',
                '........',
                '........',
                '........',
                '....K..P',
                '.......R'),
                [(5, 7), (4, 6)],
                True, False, False, False, None,
            ),
            (
                ('....k...',
                '........',
                '........',
                '........',
                '........',
                '........',
                '.....K.P',
                '.......R'),
                [(5, 7), (5, 6)],
                True, False, False, False, None,
            ),
            (
                ('....k...',
                '........',
                '........',
                '........',
                '........',
                '........',
                '......KP',
                '.......R'),
                [(5, 7), (6, 6)],
                True, False, False, False, None,
            ),
            (
                ('....k...',
                '........',
                '........',
                '........',
                '........',
                '........',
                '.......P',
                '.....KR.'),
                [(7, 7), (6, 7)],
                False, False, False, True, None,
            ),
        ]

        self.assertEqual(actual, expected)

    def test_get_every_possible_board_adds_four_boards_when_promoting(self):
        C = Chess()
        R = RetardedSloth(C)

        C.board = (
            '........',
            '.......P',
            'k.......',
            '........',
            '........',
            '........',
            '........',
            '..K.....',
        )

        actual = R.get_every_possible_board(PieceTeam.WHITE)
        expected = [
            (
                ('.......Q',
                '........',
                'k.......',
                '........',
                '........',
                '........',
                '........',
                '..K.....'),
                [(7, 1), (7, 0)],
                False, False, False, False, None,
            ),
            (
                ('.......R',
                '........',
                'k.......',
                '........',
                '........',
                '........',
                '........',
                '..K.....'),
                [(7, 1), (7, 0)],
                False, False, False, False, None,
            ),
            (
                ('.......B',
                '........',
                'k.......',
                '........',
                '........',
                '........',
                '........',
                '..K.....'),
                [(7, 1), (7, 0)],
                False, False, False, False, None,
            ),
            (
                ('.......N',
                '........',
                'k.......',
                '........',
                '........',
                '........',
                '........',
                '..K.....'),
                [(7, 1), (7, 0)],
                False, False, False, False, None,
            ),
        ]

        for board in expected:
            self.assertTrue(board in actual)

    def test_get_every_possible_board_registeres_castle(self):
        C = Chess()
        R = RetardedSloth(C)

        C.board = (
            'r...k..r',
            '........',
            '........',
            '........',
            '........',
            '........',
            '........',
            '...K....',
        )

        actual = R.get_every_possible_board(PieceTeam.BLACK)
        expected = [
            (
                ('r....rk.',
                '........',
                '........',
                '........',
                '........',
                '........',
                '........',
                '...K....'),
                [(4, 0), (7, 0)],
                True, True, False, True, None,
            ),
            (
                ('..kr...r',
                '........',
                '........',
                '........',
                '........',
                '........',
                '........',
                '...K....'),
                [(4, 0), (0, 0)],
                True, True, True, False, None,
            ),
        ]

        for board in expected:
            self.assertTrue(board in actual)


if __name__ == "__main__":
    unittest.main()
