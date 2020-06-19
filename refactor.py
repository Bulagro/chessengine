class Chess:
    """
    Wrapper for the main logic of the chess engine.
    """

    def __init__(self):
        self.set()
        self.moves = {}

        def move(f):
            self.moves.setdefault(f.__name__, f)

        # This is where we define the getters for the legal moves of each
        # piece type

        # Each function must be named by the letter representation of the
        # desired piece and have a comment specifying which piece it is

        @move
        # Pawn
        def p(self, coords=None):
            pass

        @move
        # Rook
        def r(self, coords=None):
            pass

        @move
        # Knight
        def n(self, coords=None):
            pass

        @move
        # Bishop
        def b(self, coords=None):
            pass

        @move
        # Queen
        def q(self, coords=None):
            pass

        @move
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

    def get_moves(self):
        """
        Gets all legal moves for whatever piece is in the cursor's position.
        """

        pass
