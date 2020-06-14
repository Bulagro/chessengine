from enum import Enum, auto

# Implement this shite
DEFAULT_BOARD = "Unimplemented"


class Board:
    def __init__(this):
        this.pieces = DEFAULT_BOARD

    def set(this):
        this.pieces = DEFAULT_BOARD

    def get_piece(this, x, y):
        if 0 < x < 8 and 0 < y < 8:
            return False

        return this.pieces[y][x]


Board = Board()


class Team(Enum):
    WHITE = auto()
    BLACK = auto()


class Piece:
    def __init__(this, team, board=Board):
        this.team = team
        this.board = board

    def get_moves(this):
        # Place holder, must be implemented individually per piece type
        pass


class Pawn:
    def __init__(this, team, board=Board):
        super.__init__(team, board=Board)
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
        if target is not None:
            if target.team != this.team:
                output.append(aux)

        # Attack diagonal left
        aux = (x - 1, y + this.forward)
        target = this.board.get_piece(aux[0], aux[1])
        if target is not None:
            if target.team != this.team:
                output.append(aux)

        return output
