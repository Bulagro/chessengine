import engine
import unittest


def custom_board(placement: str):
    pieces_dict = {
        # Upper case for white team
        'K': engine.Piece(engine.PieceEnum.KING, engine.Team.WHITE),
        'Q': engine.Piece(engine.PieceEnum.QUEEN, engine.Team.WHITE),
        'B': engine.Piece(engine.PieceEnum.BISHOP, engine.Team.WHITE),
        'N': engine.Piece(engine.PieceEnum.KNIGHT, engine.Team.WHITE),
        'R': engine.Piece(engine.PieceEnum.ROOK, engine.Team.WHITE),
        'P': engine.Piece(engine.PieceEnum.PAWN, engine.Team.WHITE),

        # Lower case for black team
        'k': engine.Piece(engine.PieceEnum.KING, engine.Team.BLACK),
        'q': engine.Piece(engine.PieceEnum.QUEEN, engine.Team.BLACK),
        'b': engine.Piece(engine.PieceEnum.BISHOP, engine.Team.BLACK),
        'n': engine.Piece(engine.PieceEnum.KNIGHT, engine.Team.BLACK),
        'r': engine.Piece(engine.PieceEnum.ROOK, engine.Team.BLACK),
        'p': engine.Piece(engine.PieceEnum.PAWN, engine.Team.BLACK),

        '.': None,
    }
    placement = placement.replace(' ', '').replace('\n', '').replace('\t', '')
    valid_pieces = tuple('KkQqBbNnRrPp.')

    i = 0
    board, line = [], []
    while i < len(placement):
        if placement[i] in valid_pieces:
            line.append(pieces_dict[placement[i]])

        if len(line) == 8:
            board.append(line)
            line = []

        i += 1

    board.append(line)

    return board


class TestPawnMoves(unittest.TestCase):
    def test_pawn_first_move(this):
        B = engine.Board()

        for i in range(8):
            # White
            expected_moves = [(i, 2), (i, 3)]
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
