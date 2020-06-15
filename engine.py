from enum import Enum, auto


class Board:
    def __init__(this):
        this.set()

    def set(this):
        # This is a placeholder :)
        this.pieces = [
            [Rook(Team.WHITE, this), 'WKnight', 'WBishop', 'WQueen', 'WKing', 'WBishop', 'WKnight', Rook(Team.WHITE, this)],
            [Pawn(Team.WHITE, this)] * 8
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Pawn(Team.BLACK, this)] * 8
            [Rook(Team.BLACK, this), 'BKnight', 'BBishop', 'BQueen', 'BKing', 'BBishop', 'BKnight', Rook(Team.BLACK, this)],
        ]

    def get_piece(this, x, y):
        if not (0 <= x <= 7 and 0 <= y <= 7):
            return False

        return this.pieces[y][x]


class Team(Enum):
    WHITE = auto()
    BLACK = auto()


class Piece:
    def __init__(this, team, board):
        this.team = team
        this.board = board

    def get_moves(this):
        # Place holder, must be implemented individually per piece type
        pass


class Pawn:
    def __init__(this, team, board):
        super.__init__(team, board)
        this.has_moved = False
        this.forward = 1 if team == Team.BLACK else -1

    def get_moves(this, x: int, y: int):
        output = []

        # Forward one square
        aux = (x, y + this.forward)
        if this.board.get_piece(aux[0], aux[1]) is None:
            output.append(aux)

            # Forward two sqwares
            aux = (x, y + 2 * this.forward)
            if (not this.has_moved) and this.board.get_piece(
                    aux[0], aux[1]) is None:
                output.append(aux)

        # Attack diagonal right
        aux = (x + 1, y + this.forward)
        target = this.board.get_piece(aux[0], aux[1])
        if target and target.team != this.team:
            output.append(aux)

        # Attack diagonal left
        aux = (x - 1, y + this.forward)
        target = this.board.get_piece(aux[0], aux[1])
        if target and target.team != this.team:
            output.append(aux)

        return output


class Rook(Piece):
    def __init__(this, team, board):
        super.__init__(team, board)

    def get_moves(this, x, y):
        output = []
        for tempname in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
            i = 1
            while (target := this.board.get_piece(
                (tx := x + tempname[0] * i),
                (ty := y + tempname[1] * i))
            ) is None:
                i += 1
                output.append((tx, ty))
            else:
                if target and target.team != this.team:
                    output.append((tx, ty))
