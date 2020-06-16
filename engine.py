from enum import Enum, auto


class Team(Enum):
    WHITE = auto()
    BLACK = auto()


class PieceEnum(Enum):
    PAWN = auto()
    ROOK = auto()
    KNIGHT = auto()
    BISHOP = auto()
    QUEEN = auto()
    KING = auto()


class Board:
    def __init__(this):
        this.set()

    def set(this):
        # This is NOT a placeholder :)
        this.pieces = [
            [
                Piece(PieceEnum.ROOK, Team.WHITE),
                Piece(PieceEnum.KNIGHT, Team.WHITE),
                Piece(PieceEnum.BISHOP, Team.WHITE),
                Piece(PieceEnum.QUEEN, Team.WHITE),
                Piece(PieceEnum.KING, Team.WHITE),
                Piece(PieceEnum.BISHOP, Team.WHITE),
                Piece(PieceEnum.KNIGHT, Team.WHITE),
                Piece(PieceEnum.ROOK, Team.WHITE),
            ],
            [Piece(PieceEnum.PAWN, Team.WHITE)] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Piece(PieceEnum.PAWN, Team.BLACK)] * 8,
            [
                Piece(PieceEnum.ROOK, Team.WHITE),
                Piece(PieceEnum.KNIGHT, Team.WHITE),
                Piece(PieceEnum.BISHOP, Team.WHITE),
                Piece(PieceEnum.QUEEN, Team.WHITE),
                Piece(PieceEnum.KING, Team.WHITE),
                Piece(PieceEnum.BISHOP, Team.WHITE),
                Piece(PieceEnum.KNIGHT, Team.WHITE),
                Piece(PieceEnum.ROOK, Team.WHITE),
            ],
        ]

    def get_piece(this, x: int, y: int):
        if not (0 <= x <= 7 and 0 <= y <= 7):
            return False

        piece = this.pieces[y][x]
        return None if not piece else piece.get()

    def get_pawn_moves(this, x: int, y: int):
        if p := this.get_piece(x, y):
            forward = -1 if p['team'] == Team.BLACK else 1
            has_moved = (y != (6 if p['team'] == Team.BLACK else 1))
            output = []

            # Forward one square
            aux = (x, y + forward)
            if this.get_piece(aux[0], aux[1]) is None:
                output.append(aux)

                # Forward two sqwares
                aux = (x, y + 2 * forward)
                if (not has_moved) and this.get_piece(
                        aux[0], aux[1]) is None:
                    output.append(aux)

            # Attack diagonal right
            aux = (x + 1, y + forward)
            target = this.get_piece(aux[0], aux[1])
            if target and target['team'] != p['team']:
                output.append(aux)

            # Attack diagonal left
            aux = (x - 1, y + forward)
            target = this.get_piece(aux[0], aux[1])
            if target and target['team'] != p['team']:
                output.append(aux)

            return output

        # Invalid pos (OOB)
        return None

    def get_rook_moves(this, x: int, y: int):
        if p := this.get_piece(x, y):
            output = []
            for tempname in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                i = 1
                while (target := this.get_piece(
                    (tx := x + tempname[0] * i),
                    (ty := y + tempname[1] * i))
                ) is None:
                    i += 1
                    output.append((tx, ty))
                else:
                    if target and target['team'] != p['team']:
                        output.append((tx, ty))

            return output
        return None

    def move_piece(this, x, y):
        move_map = {
            PieceEnum.PAWN: this.get_pawn_moves,
            PieceEnum.ROOK: this.get_rook_moves,
            None: [],
        }

        piece = this.get_piece(x, y)

        return move_map[piece[0]](x, y, piece[1]) if piece else []


class Piece:
    def __init__(this, name: PieceEnum, team: Team):
        this.name = name
        this.team = team

    def get(this):
        return {
            'name': this.name,
            'team': this.team,
        }
