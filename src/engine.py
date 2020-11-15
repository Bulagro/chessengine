"""
This is The Bad Chess Engine.
It gives you the tools to make a usable chess game.

The logic is contained in the 'Chess' class.
From this class you'll use:
- get_piece_moves() to get some piece's moves
- get_king_status() to determine tie, check or checkmate,
    avaliable moves to protect against that check and
    pinned pieces (and their possible moves).
- move_piece() to change the position between two pieces.
- replace_piece() to turn a piece into another or add a new one.

Additionally, there are variables such as has_king_moved and has_rook_moved,
    used to determine whether a castle (move) is possible.
"""


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
        self.tie = False
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
        - consider_pins: takes pinned pieces into consideration.
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

        if not self.can_move(team):
            if self.in_check == team:
                self.checkmate = team
            else:
                self.tie = True

        else: # Check if there're only kings
            for line in self.board:
                line = line.replace('.', '')
                if line != 'k' and line != 'K':
                    return None
            else:
                self.tie = True


    def get_every_square_the_king_cant_be_in(self, team: PieceTeam, count_pieces=False):
        squares = []
        pieces_dict = {
            PieceName.KING   : 0,
            PieceName.QUEEN  : 0,
            PieceName.BISHOP : 0,
            PieceName.KNIGHT : 0,
            PieceName.ROOK   : 0,
            PieceName.PAWN   : 0,
        }

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

                if piece == EMPTY_SQUARE:
                    continue
                elif piece[1] == team:
                    if count_pieces:
                        pieces_dict[piece[0]] += 1
                    continue

                if piece[0] == PieceName.PAWN:
                    squares += self.p_attack(j, i, oposing_team, show_protected=True)
                else:
                    squares += PIECE_MOVES[piece[0]](j, i, show_protected=True)

        if count_pieces:
            return (squares, pieces_dict)

        return squares


    def can_move(self, team: PieceTeam):
        """
        Returns a boolean value: whether a team can move or not.
        """

        for y in range(8):
            for x in range(8):
                piece_name, piece_team = self.get_piece(x, y)

                if piece_name != None and piece_team == team:
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

        self.in_check = None
        self.checkmate = None
        self.tie = False
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


    def replace_piece(self, x: int, y: int, name: PieceName, team: PieceTeam):
        piece_dict = {
            PieceName.KING   : 'k',
            PieceName.QUEEN  : 'q',
            PieceName.ROOK   : 'r',
            PieceName.BISHOP : 'b',
            PieceName.KNIGHT : 'n',
            PieceName.PAWN   : 'p',
        }

        new_board = list(self.board)
        line = list(new_board[y])
        line[x] = piece_dict[name]

        if team == PieceTeam.WHITE:
            line[x] = line[x].upper()

        new_board[y] = ''.join(line)
        self.board = tuple(new_board)


class Node:
    def __init__(self, score, king_moved, lrook_moved, rrook_moved, children):
        self.score       = score
        self.king_moved  = king_moved
        self.lrook_moved = lrook_moved
        self.rrook_moved = rrook_moved
        self.children    = children


class RetardedSloth:
    """
    The terrible AI that's supposed to play against the player... actually with.
    """

    def __init__(self, engine):
        self.engine = engine
        self.piece_value_dict = {
            PieceName.PAWN   : 1,
            PieceName.KNIGHT : 2,
            PieceName.BISHOP : 3,
            PieceName.ROOK   : 5,
            PieceName.QUEEN  : 9,
            PieceName.KING   : 0,
            None             : 0,
        }
        self.team = PieceTeam.BLACK
        self.max_level = 1


    def configure(self):
        """
        Changes the Sloth's behaviour.
        """

        pass


    def get_next_move(self):
        """
        Returns a list with two tuples: [(ox, oy), (dx, dy)].
        """

        def traverse_assign(node: Node, find_min: bool):
            if not node.children:
                return None

            for child in node.children:
                traverse_assign(child, not find_min)

            scores = (child.score for child in node.children)
            node.score = min(scores) if find_min else max(scores)

            return node.score


        root, first_moves = self.generate_moves_tree(self.team, self.max_level)
        move_score = traverse_assign(root, False)
        print(move_score)

        move_index = [child.score for child in root.children].index(move_score)

        return first_moves[move_index]

    def generate_moves_tree(self, original_team: PieceTeam, max_level: int):
        """
        Returns a <Node()> containing every possible move from a given position.
        """

        def add_children(node: Node, team: PieceTeam, evaluate_board: bool):
            boards = self.get_every_possible_board(team)
            moves = []

            for board in boards:
                position, move, k, castle, lr, rr, ep = board
                old_lr = self.engine.has_rook_moved[team.value - 1][0]
                old_rr = self.engine.has_rook_moved[team.value - 1][1]
                old_k  = self.engine.has_king_moved[team.value - 1]
                old_p  = self.engine.board

                self.engine.board = position
                self.engine.has_rook_moved[team.value - 1][0] = lr
                self.engine.has_rook_moved[team.value - 1][1] = rr
                self.engine.has_king_moved[team.value - 1]    = k

                if evaluate_board:
                    score = self.evaluate_board(team, ep)
                else:
                    score = 1

                self.engine.board = old_p
                self.engine.has_king_moved[team.value - 1]    = old_k
                self.engine.has_rook_moved[team.value - 1][0] = old_lr
                self.engine.has_rook_moved[team.value - 1][1] = old_rr


                node.children.append(
                    Node(score, k, lr, rr, [])
                )

                moves += [(move, castle)]

            return moves

        def traverse_make(node: Node, level: int, team: PieceTeam):
            first_moves = None

            if level < max_level:
                average_score = sum(child.score for child in node.children) / len(node.children) if node.children else 0
                level += 1
                first_moves = add_children(node, team, True)

                for child in node.children:
                    if node.children: # First attempt at optimization.
                        if team == original_team:
                            if node.score < average_score: continue
                        else:
                            if node.score > average_score: continue

                    if child.score <= 0: # Don't analyze node that ends the game (checkmate or tie).
                        continue

                    traverse_make(child, level, PieceTeam.BLACK if team == PieceTeam.WHITE else PieceTeam.WHITE)

            return first_moves


        root = Node(0,
                    self.engine.has_king_moved[original_team.value - 1],
                    self.engine.has_rook_moved[original_team.value - 1][0],
                    self.engine.has_rook_moved[original_team.value - 1][1],
                    []
        )
        first_moves = traverse_make(root, 0, original_team)

        return root, first_moves


    def get_every_possible_board(self, team: PieceTeam):
        boards = [] # This contains tuples like this one:
                    # (<board>, [move], <king moved>, <is_castle>, <lrook moved>, <rrook moved>, <eaten piece>)

        for oy in range(8):
            for ox in range(8):
                origin_name, origin_team = self.engine.get_piece(ox, oy)

                if origin_team == team:
                    origin_team_y = 0 if team == PieceTeam.BLACK else 7

                    for move in self.engine.get_piece_moves(ox, oy, consider_pins=True):
                        dx, dy = move
                        dest_name, dest_team = self.engine.get_piece(dx, dy)
                        rrook_moved, lrook_moved, king_moved = False, False, False

                        eaten_piece = dest_name
                        promotion = origin_name == PieceName.PAWN and (dy == (0 if origin_team == PieceTeam.WHITE else 7))
                        is_castle = origin_name == PieceName.KING and dest_name == PieceName.ROOK and dest_team == origin_team

                        if origin_name == PieceName.KING:
                            king_moved = True
                        elif origin_name == PieceName.ROOK:
                            if ox == 0 and oy == origin_team_y:
                                lrook_moved = True
                            elif ox == 7 and oy == origin_team_y:
                                rrook_moved = True

                        if is_castle:
                            if dx == 0:
                                lrook_moved = True
                            else:
                                rrook_moved = True

                            eaten_piece = None

                        old_board = self.engine.board
                        self.engine.move_piece(ox, oy, dx, dy, is_castle)

                        if promotion:
                            for piece in (PieceName.QUEEN, PieceName.ROOK, PieceName.BISHOP, PieceName.KNIGHT):
                                self.engine.replace_piece(dx, dy, piece, origin_team)
                                boards += [(self.engine.board, [(ox, oy), (dx, dy)], False, False, False, False, eaten_piece)]

                            self.engine.board = old_board
                            continue

                        boards += [(self.engine.board, [(ox, oy), (dx, dy)], king_moved, is_castle, lrook_moved, rrook_moved, eaten_piece)]
                        self.engine.board = old_board

        return boards


    def evaluate_board(self, team: PieceTeam, eaten_piece: PieceName):
        """
        Returns given a borad, returns it's score.
        """

        opposing_team = PieceTeam.WHITE if team == PieceTeam.BLACK else PieceTeam.BLACK
        self.engine.get_king_status(opposing_team)

        if self.engine.checkmate == team:
            return -1000
        elif self.engine.checkmate != None and self.engine.checkmate != team:
            return 1000
        elif self.engine.tie:
            return 0

        # oking stands for "Opposing Team's King".
        squares_the_oking_cant_be_in, pieces_count = self.engine.get_every_square_the_king_cant_be_in(opposing_team, True)
        oking_x, oking_y = self.engine.find_king_pos(opposing_team)

        score = 0
        for piece in pieces_count:
            score += self.piece_value_dict[piece]

        center_control_points_dict = {
            (2, 2) : 1, (3, 2) : 1, (4, 2) : 1, (5, 2) : 1,
            (2, 5) : 1, (3, 5) : 1, (4, 5) : 1, (5, 5) : 1,
            (3, 3) : 2, (4, 3) : 2, (3, 4) : 2, (4, 4) : 2,
        }

        king_threat_dict = {
            (oking_x + 1, oking_y) : 2, (oking_x - 1, oking_y) : 2,
            (oking_x, oking_y + 1) : 2, (oking_x, oking_y - 1) : 2,
            (oking_x + 1, oking_y + 1) : 2, (oking_x - 1, oking_y - 1) : 2,
            (oking_x + 1, oking_y - 1) : 2, (oking_x - 1, oking_y + 1) : 2,

            (oking_x + 2, oking_y) : 1, (oking_x - 2, oking_y) : 1,
            (oking_x, oking_y + 2) : 1, (oking_x, oking_y - 2) : 1,
            (oking_x + 2, oking_y + 2) : 1, (oking_x - 2, oking_y - 2) : 1,
            (oking_x + 2, oking_y - 2) : 1, (oking_x - 2, oking_y + 2) : 1,
        }

        for pos in squares_the_oking_cant_be_in:
            for d in (center_control_points_dict, king_threat_dict):
                if pos in d:
                    score += d[pos]

        if self.engine.in_check == opposing_team:
            return 500

        score += self.piece_value_dict[eaten_piece]
        score += len(self.engine.pinned_pieces)

        return score
