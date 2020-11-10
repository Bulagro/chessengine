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
                True, True, True, False, None,
            ),
        ]

        for board in expected:
            self.assertTrue(board in actual)


if __name__ == "__main__":
    unittest.main()
