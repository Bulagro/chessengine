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
        self.in_check = None
        self.checkmate = None
        self.moves_to_defend_check = []
        self.pinned_pieces = {}

                            #  White  Black
        self.has_king_moved = [False, False]
        self.has_rook_moved = [[False, False], [False, False]]
                            #  WL      WR      BL      BR
        self.set()

    def get_piece_moves(self, x: int, y: int, show_protected=False, consider_pins=False):
        """
        Returns every legal move for a specific piece, given a position.
        - show_protected: add those squares protected by the selected piece.
        - consider_pins:  takes pinned pieces into consideration.
        """

        PIECE_MOVES = {
            PieceName.KING   : self.k,
            PieceName.QUEEN  : self.q,
            PieceName.BISHOP : self.b,
            PieceName.KNIGHT : self.n,
            PieceName.ROOK   : self.r,
            PieceName.PAWN   : self.p,
        }

        piece_name, piece_team = self.get_piece(x, y)

        if piece_name == None:
            return []

        piece_moves = PIECE_MOVES[piece_name](x, y, show_protected)

        if consider_pins:
            if (x, y) in self.pinned_pieces:
                possible_moves = self.pinned_pieces[(x, y)]
                piece_moves = [move for move in piece_moves if move in possible_moves]

        if self.in_check == piece_team and piece_name != PieceName.KING:
            piece_moves = [move for move in piece_moves if move in self.moves_to_defend_check]

        return piece_moves


    # Pawn moves
    def p(self, x: int, y: int, show_protected=False):
        p = self.get_piece(x, y)
        if p:
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

            output += self.p_attack(x, y, piece_team, show_protected)
            return output

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
        p = self.get_piece(x, y)
        if p:
            _, piece_team = p
            output = []

            for tempname in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                i = 1
                tx = x + tempname[0]
                ty = y + tempname[1]
                target = self.get_piece(tx, ty)

                while target and target[1] != piece_team:
                    i += 1

                    if target == EMPTY_SQUARE:
                        output.append((tx, ty))
                    else:
                        if target[0] != PieceName.KING:
                            output.append((tx, ty))
                        if not show_protected or target[0] != PieceName.KING:
                            break

                    tx = x + tempname[0] * i
                    ty = y + tempname[1] * i
                    target = self.get_piece(tx, ty)
                else:
                    if target:
                        target_name, _ = target

                        # Protected pieces
                        if show_protected and target_name != PieceName.KING:
                            output.append((tx, ty))

            return output
        return None


    # Knight moves
    def n(self, x: int, y: int, show_protected=False):
        p = self.get_piece(x, y)
        if p:
            _, piece_team = p
            output = []

            for tempname in [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
                tx = x + tempname[0]
                ty = y + tempname[1]
                target = self.get_piece(tx, ty)

                if target is None:
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
        p = self.get_piece(x, y)
        if p:
            _, piece_team = p
            output = []

            for tempname in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                i = 1
                tx = x + tempname[0]
                ty = y + tempname[1]
                target = self.get_piece(tx, ty)

                while target and target[1] != piece_team:
                    i += 1

                    if target == EMPTY_SQUARE:
                        output.append((tx, ty))
                    else:
                        if target[0] != PieceName.KING:
                            output.append((tx, ty))
                        if not show_protected or target[0] != PieceName.KING:
                            break

                    tx = x + tempname[0] * i
                    ty = y + tempname[1] * i
                    target = self.get_piece(tx, ty)
                else:
                    if target:
                        target_name, _ = target

                        # Protected pieces
                        if show_protected and target_name != PieceName.KING:
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
        p = self.get_piece(x, y)
        if p:
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

            if not show_protected:
                bad_squares = self.get_every_square_the_king_cant_be_in(piece_team)
                king_moves = [move for move in king_moves if move not in bad_squares]

                p = piece_team.value - 1
                king_y = 0 if piece_team == PieceTeam.BLACK else 7

                # Castling!
                if not self.has_king_moved[p] and self.in_check != piece_team:
                    r = self.get_piece(0, king_y)
                    if not self.has_rook_moved[p][0] and r[0] == PieceName.ROOK and r[1] == piece_team:
                        for x in range(3, 0, -1):
                            if (x, king_y) in bad_squares or self.get_piece(x, king_y) != EMPTY_SQUARE:
                                break
                        else:
                            king_moves.append((0, king_y))

                    r = self.get_piece(7, king_y)
                    if not self.has_rook_moved[p][1] and r[0] == PieceName.ROOK and r[1] == piece_team:
                        for x in range(5, 7):
                            if (x, king_y) in bad_squares or self.get_piece(x, king_y) != EMPTY_SQUARE:
                                break
                        else:
                            king_moves.append((7, king_y))

            return king_moves

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
            tx = kx + tempname[0]
            ty = ky + tempname[1]
            target = self.get_piece(tx, ty)

            while target:
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
                tx = kx + tempname[0] * i
                ty = ky + tempname[1] * i
                target = self.get_piece(tx, ty)

        # Diagonal line.
        for tempname in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            path = []
            remembered_piece = None

            i = 1
            tx = kx + tempname[0]
            ty = ky + tempname[1]
            target = self.get_piece(tx, ty)

            while target:

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
                tx = kx + tempname[0] * i
                ty = ky + tempname[1] * i
                target = self.get_piece(tx, ty)

        # Knights
        for tempname in [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            tx = kx + tempname[0]
            ty = ky + tempname[1]
            target = self.get_piece(tx, ty)

            if target:
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

        if not self.can_move(team) and self.in_check == team:
            self.checkmate = team


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

                if piece == EMPTY_SQUARE or piece[1] == team: continue

                if piece[0] == PieceName.PAWN:
                    squares += self.p_attack(j, i, oposing_team, show_protected=True)
                else:
                    squares += PIECE_MOVES[piece[0]](j, i, show_protected=True)

        return squares


    def can_move(self, team: PieceTeam):
        """
        Returns a boolean value: whether a team can move or not.
        """

        for y in range(8):
            for x in range(8):
                piece_name, piece_team = self.get_piece(x, y)

                if piece_name and piece_team == team:
                    if self.get_piece_moves(x, y, consider_pins=True):
                        return True

        return False


    def move_piece(self, ox: int, oy: int, dx: int, dy: int, castle: bool):
        """
        Replaces characters on the board without performing any checks.
        """

        origin_line = list(self.board[oy])
        destiny_line = list(self.board[dy])

        if castle: # origin = king, destiny = rook
            castle_dir = 1
            if dx < ox: castle_dir = -1

            king_x = ox + (2 * castle_dir)

            destiny_line[ox] = '.'
            destiny_line[dx] = '.'
            destiny_line[king_x] = self.board[oy][ox]
            destiny_line[king_x + (1 * castle_dir * -1)] = self.board[dy][dx]
        else:
            if oy == dy:
                destiny_line[ox] = '.'

            origin_line[ox] = '.'
            destiny_line[dx] = self.board[oy][ox]

        new_board = list(self.board)
        new_board[oy] = ''.join(origin_line)
        new_board[dy] = ''.join(destiny_line)

        self.board = tuple(new_board)


    def set(self):
        """
        Resets the board to it's default layout and the cursor to its default
        position.
        """

        self.cursor = [0, 0]

        self.in_check = None
        self.checkmate = None
        self.moves_to_defend_check = []
        self.pinned_pieces = {}
        self.has_king_moved = [False, False]
        self.has_rook_moved = [[False, False], [False, False]]

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


    def get_piece(self, x: int, y: int):
        """
        Returns the piece in the given x, y coordinate.
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

    def replace_piece(x: int, y: int, name: PieceName, team: PieceTeam):
        piece_dict = {
            PieceName.KING   : 'k',
            PieceName.QUEEN  : 'q',
            PieceName.ROOK   : 'r',
            PieceName.BISHOP : 'b',
            PieceName.KNIGHT : 'n',
            PieceName.PAWN   : 'p',
        }

        new_board = list(self.board)
        new_board[y][x] = piece_dict[name]

        if team == PieceTeam.WHITE:
            new_board[y][x] = new_board[y][x].upper()