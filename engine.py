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


EMPTY_SQUARE = (None, None)


class Chess:
    """
    Wrapper for the main logic of the chess engine.
    """

    def __init__(self):
        self.set()
        self.in_check = None


    def get_piece_moves(self, x: int, y: int, show_protected=False):
        """
        Returns every legal move for a specific piece, given a position.
        - show_protected: add those squares protected by the selected piece.
        """

        PIECE_MOVES = {
            PieceName.KING   : self.k,
            PieceName.QUEEN  : self.q,
            PieceName.BISHOP : self.b,
            PieceName.KNIGHT : self.n,
            PieceName.ROOK   : self.r,
            PieceName.PAWN   : self.p,
        }

        p = self.get_piece(x, y)
        return PIECE_MOVES[p[0]](x, y, show_protected)


    # Pawn moves
    def p(self, x: int, y: int, show_protected=False):
        if p := self.get_piece(x, y):
            _, piece_team = p

            forward = 1 if piece_team == PieceTeam.BLACK else -1
            has_moved = y != (1 if piece_team == PieceTeam.BLACK else 6)
            output = []

            # Forward one square
            aux = (x, y + forward)
            if self.get_piece(aux[0], aux[1]) == EMPTY_SQUARE:
                output.append(aux)

                # Forward two sqwares
                aux = (x, y + 2 * forward)
                if (not has_moved) and self.get_piece(aux[0], aux[1]) == EMPTY_SQUARE:
                    output.append(aux)

            return output + self.p_attack(x, y, piece_team, show_protected)

        # Invalid pos (OOB)
        return False


    def p_attack(self, x: int, y: int, team: PieceTeam, show_protected=False):
        output = []
        forward = 1 if team == PieceTeam.BLACK else -1

        for aux in [(x + 1, y + forward), (x - 1, y + forward)]:
            target = self.get_piece(aux[0], aux[1])
            if target:
                target_name, target_team = target

                if ((target != EMPTY_SQUARE and target_team != team and target_name != PieceName.KING) or
                (target == EMPTY_SQUARE and show_protected)):
                    output.append(aux)

                # Add protected pieces to the list
                if show_protected and target_team == team and target_name != PieceName.KING:
                    output.append(aux)

        return output


    # Rook moves
    def r(self, x: int, y: int, show_protected=False):
        if p := self.get_piece(x, y):
            _, piece_team = p
            output = []

            for tempname in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                i = 1
                while (target := self.get_piece(
                    (tx := x + tempname[0] * i),
                    (ty := y + tempname[1] * i))) is EMPTY_SQUARE:
                    i += 1
                    output.append((tx, ty))
                else:
                    if target:
                        target_name, target_team = target

                        if target_team != piece_team and target_name != PieceName.KING:
                            output.append((tx, ty))

                    # Protected pieces
                        if show_protected and target_team == piece_team and target_name != PieceName.KING:
                            output.append((tx, ty))

            return output
        return None


    # Knight moves
    def n(self, x: int, y: int, show_protected=False):
        if p := self.get_piece(x, y):
            _, piece_team = p
            output = []

            for tempname in [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
                if (target := self.get_piece(
                        (tx := x + tempname[0]),
                        (ty := y + tempname[1]))) is None:
                    output.append((tx, ty))
                else:
                    if target:
                        target_name, target_team = target

                        if target_team != piece_team and target_name != PieceName.KING:
                            output.append((tx, ty))

                        # Protected pieces
                        if show_protected and target_team == piece_team and target_name != PieceName.KING:
                            output.append((tx, ty))

            return output
        return None


    # Bishop moves
    def b(self, x: int, y: int, show_protected=False):
        if p := self.get_piece(x, y):
            _, piece_team = p
            output = []

            for tempname in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                i = 1
                while (target := self.get_piece(
                    (tx := x + tempname[0] * i),
                    (ty := y + tempname[1] * i))) is EMPTY_SQUARE:
                    i += 1
                    output.append((tx, ty))
                else:
                    if target:
                        target_name, target_team = target

                        if target_team != piece_team and target_name != PieceName.KING:
                            output.append((tx, ty))

                        # Protected pieces
                        if show_protected and target_team == piece_team and target_name != PieceName.KING:
                            output.append((tx, ty))

            return output
        return None


    # Queen moves
    def q(self, x: int, y: int, show_protected=False):
        diagonal = self.b(x, y, show_protected)
        straight = self.r(x, y, show_protected)

        if diagonal == EMPTY_SQUARE or straight == EMPTY_SQUARE:
            return EMPTY_SQUARE
        else:
            return straight + diagonal


    # King moves
    def k(self, x: int, y: int, show_protected=False):
        if p := self.get_piece(x, y):
            _, piece_team = p
            king_moves = []

            for tempname in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                tx = x + tempname[0]
                ty = y + tempname[1]
                target = self.get_piece(tx, ty)

                if target:
                    _, target_team = target

                    if target == EMPTY_SQUARE:
                        king_moves.append((tx, ty))

                    elif target_team != piece_team:
                        king_moves.append((tx, ty))

                    # Protected pieces
                    elif show_protected and target_team == piece_team:
                        king_moves.append((tx, ty))

            if show_protected:
                return king_moves
            else:
                bad_squares = self.get_every_square_the_king_cant_be_in(piece_team)
                return [move for move in king_moves if move not in bad_squares]

        return None


    def find_king_pos(self, team: PieceTeam):
        """
        Where's the king?
        """
        king_to_look_for = 'k' if team == PieceTeam.BLACK else 'K'

        for i, p in enumerate(self.board):
            for j in range(8):
                if p[j] == king_to_look_for:
                    return (j, i)

        raise ValueError('How tf is there no king on the board?')


    def get_king_status(self, team: PieceTeam):
        """
        Sets the in_check flag, pinned_pieces and a list of moves
        to defend the check.
        """

        # Clear values of previous position.
        self.in_check = None
        self.moves_to_defend_check = []
        self.pinned_pieces = {}

        kx, ky = self.find_king_pos(team)
        forward = 1 if team == PieceTeam.BLACK else -1

        # Straight line.
        for tempname in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            path = []
            remembered_piece = None
            i = 1

            while (target := self.get_piece(
                (tx := kx + tempname[0] * i),
                (ty := ky + tempname[1] * i))):

                target_name, target_team = target

                if target == EMPTY_SQUARE:
                    path.append((tx, ty))

                elif target_team == team:
                    if remembered_piece: break
                    else: remembered_piece = (tx, ty)

                else: # target_team != team
                    if target_name in (PieceName.ROOK, PieceName.QUEEN):
                        path.append((tx, ty))

                        # Pin
                        if remembered_piece:
                            rx, ry = remembered_piece
                            self.pinned_pieces[remembered_piece] = [
                                move for move in self.get_piece_moves(rx, ry)
                                if move in path
                            ]
                            break

                        # Check
                        else:
                            self.moves_to_defend_check += path
                            self.in_check = team
                            break
                    else:
                        break
                i += 1

        # Diagonal line.
        for tempname in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            path = []
            remembered_piece = None
            i = 1

            while (target := self.get_piece(
                (tx := kx + tempname[0] * i),
                (ty := ky + tempname[1] * i))):

                target_name, target_team = target

                if target == EMPTY_SQUARE:
                    path.append((tx, ty))

                elif target_team == team:
                    if remembered_piece: break
                    else: remembered_piece = (tx, ty)

                else: # target_team != team
                    if target_name in (PieceName.BISHOP, PieceName.QUEEN):
                        path.append((tx, ty))

                        # Pin
                        if remembered_piece:
                            rx, ry = remembered_piece
                            self.pinned_pieces[remembered_piece] = [
                                move for move in self.get_piece_moves(rx, ry)
                                if move in path
                            ]
                            break

                        # Check
                        else:
                            self.moves_to_defend_check += path
                            self.in_check = team
                            break
                    else:
                        break
                i += 1

        # Knights
        for tempname in [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            if (target := self.get_piece(
                (tx := kx + tempname[0]),
                (ty := ky + tempname[1]))):

                target_name, target_team = target

                if target_name == PieceName.KNIGHT and target_team != team:
                    self.in_check = team
                    self.moves_to_defend_check = [(tx, ty)]

        # Pawns
        for i in (1, -1):
            target = self.get_piece(kx + i, ky + forward)
            if not target or target == EMPTY_SQUARE: continue

            target_name, target_team = target

            if target_name == PieceName.PAWN and target_team != team:
                self.in_check = team
                self.moves_to_defend_check = [(kx + i, ky + forward)]


    def get_every_square_the_king_cant_be_in(self, team: PieceTeam):
        squares = []
        oposing_team = PieceTeam.BLACK if team == PieceTeam.WHITE else PieceTeam.WHITE

        PIECE_MOVES = {
            PieceName.KING   : self.k,
            PieceName.QUEEN  : self.q,
            PieceName.BISHOP : self.b,
            PieceName.KNIGHT : self.n,
            PieceName.ROOK   : self.r,
        }

        for i in range(8):
            for j in range(8):
                piece = self.get_piece(j, i)

                if (
                    not piece             or
                    piece == EMPTY_SQUARE or
                    piece[1] == team
                    ): continue

                if piece[0] == PieceName.PAWN:
                    squares += self.p_attack(j, i, oposing_team, show_protected=True)
                else:
                    squares += PIECE_MOVES[piece[0]](j, i, show_protected=True)

        return squares


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
            '.' : EMPTY_SQUARE,
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
