from enum import Enum, auto

class PieceTeam(Enum):
    WHITE = auto()
    BLACK = auto()

class PieceName(Enum):
    KING   = auto()
    QUEEN  = auto()
    BISHOP = auto()
    KNIGHT = auto()
    ROOK   = auto()
    PAWN   = auto()


class Chess:
    """
    Wrapper for the main logic of the chess engine.
    """

    def __init__(self):
        self.set()
        self.moves = {}

    def get_piece_moves(f):
        self.moves.setdefault(f.__name__, f)

        # This is where we define the getters for the legal moves of each
        # piece type

        # Each function must be named by the letter representation of the
        # desired piece and have a comment specifying which piece it is

    @get_piece_moves
    # Pawn
    def p(self, coords=None):
        return 'p'

    @get_piece_moves
    # Rook
    def r(self, coords=None):
        pass

    @get_piece_moves
    # Knight
    def n(self, coords=None):
        pass

    @get_piece_moves
    # Bishop
    def b(self, coords=None):
        pass

    @get_piece_moves
    # Queen
    def q(self, coords=None):
        pass

    @get_piece_moves
    # King
    def k(self, coords=None):
        pass

    def set(self):
        """
        Resets the board to it's default layout and the cursor to its default
        position.
        """

        self.cursor = [0, 0]
        self.board = (
            'rnbqkbnr',
            'pppppppp',
            '........',
            '........',
            '........',
            '........',
            'PPPPPPPP',
            'RNBQKBNR',
        )

    def move_cursor(self, x, y):
        """
        Moves the cursor by the specified amount if possible.
        """

        if 0 <= (aux := self.cursor[0] + x) <= 7:
            self.cursor[0] = aux

        if 0 <= (aux := self.cursor[1] + y) <= 7:
            self.cursor[1] = aux

    def get_piece(self, x: int, y: int):
        """
        Returns the piece the cursor's pointing at.
        """

        piece_info = {
            'p' : (PieceName.PAWN,   PieceTeam.BLACK),
            'P' : (PieceName.PAWN,   PieceTeam.WHITE),
            'r' : (PieceName.ROOK,   PieceTeam.BLACK),
            'R' : (PieceName.ROOK,   PieceTeam.WHITE),
            'n' : (PieceName.KNIGHT, PieceTeam.BLACK),
            'N' : (PieceName.KNIGHT, PieceTeam.WHITE),
            'b' : (PieceName.BISHOP, PieceTeam.BLACK),
            'B' : (PieceName.BISHOP, PieceTeam.WHITE),
            'q' : (PieceName.QUEEN,  PieceTeam.BLACK),
            'Q' : (PieceName.QUEEN,  PieceTeam.WHITE),
            'k' : (PieceName.KING,   PieceTeam.BLACK),
            'K' : (PieceName.KING,   PieceTeam.WHITE),
            '.' : None,
        }

        if 0 <= x <= 7 and 0 <= y <= 7:
            return piece_info[self.board[y][x]]
        else:
            return False

    def get_moves(self):
        """
        Gets all legal moves for whatever piece is in the cursor's position.
        """

        pass
