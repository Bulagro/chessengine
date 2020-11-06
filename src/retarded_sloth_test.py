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


if __name__ == "__main__":
    unittest.main()
