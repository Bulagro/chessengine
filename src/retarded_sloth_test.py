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
                False,
                False,
                False,
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
                False,
                False,
                False,
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
                False,
                False,
                False,
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
if __name__ == "__main__":
    unittest.main()
