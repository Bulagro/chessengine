import engine
import unittest

class TestPawnMoves(unittest.TestCase):
    def test_pawn_first_move(this):
        B = engine.Board()

        for i in range(8):
            # White
            expected_moves = [(i, 2), (i,3)]
            actual_moves = B.get_pawn_moves(i, 1)

            this.assertEqual(expected_moves, actual_moves)

            # Black
            expected_moves = [(i, 5), (i, 4)]
            actual_moves = B.get_pawn_moves(i, 6)

            this.assertEqual(expected_moves, actual_moves)

    def test_invalid_pawn_pos(this):
        B = engine.Board()

        expected_moves = None
        actual_moves = B.get_pawn_moves(-1, -1)

        this.assertEqual(expected_moves, actual_moves)

    @unittest.skip("Unimplemented")
    def test_pawn_attacking_moves(this):
        pass

    @unittest.skip("Unimplemented")
    def test_pinned_pawn(this):
        pass

    def test_wrook_move(this):
        B = engine.Board()

        expected_moves = []
        actual_moves = B.get_rook_moves(0, 0)

        this.assertEqual(expected_moves, actual_moves)

    @unittest.skip("Unimplemented")
    def test_rook_free_movement(this):
        pass


if __name__ == "__main__":
    unittest.main()
