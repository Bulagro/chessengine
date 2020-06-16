import engine
import unittest


def custom_board(board: str):
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
    board = board.replace(' ', '').replace('\n', '').replace('\t', '')
    valid_pieces = tuple('KkQqBbNnRrPp.')

    return [
        [pieces_dict[board[8 * i + j]] for j in range(8) if board[8 * i + j] in valid_pieces]
        for i in range(8)
        ]


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

    def test_pawn_single_attack_move(this):
        B = engine.Board()
        B.pieces = custom_board(
            """
            ........
            ........
            ........
            ........
            ...P....
            ..p.....
            ........
            ........
            """)

        # White
        expected_moves = [(3, 5), (2, 5)]
        actual_moves = B.get_pawn_moves(3, 4)

        this.assertEqual(expected_moves, actual_moves)

        # Black
        expected_moves = [(2, 4), (3, 4)]
        actual_moves = B.get_pawn_moves(2, 5)

        this.assertEqual(expected_moves, actual_moves)


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
