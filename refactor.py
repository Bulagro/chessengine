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
            pass

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

        if 0 <= x <= 7 and 0 <= y <= 7:
            return self.board[y][x]
        else:
            return None

    def get_moves(self):
        """
        Gets all legal moves for whatever piece is in the cursor's position.
        """

        pass
