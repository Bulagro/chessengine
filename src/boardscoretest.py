from engine import *


def evaluate_board(engine: Chess, team: PieceTeam, eaten_piece: PieceName):
    engine.get_king_status(team)

    if engine.checkmate == team:
        return -1000
    elif engine.checkmate and engine.checkmate != team:
        return 1000
    elif engine.tie:
        return 0

    score = 0
    opposing_team = PieceTeam.WHITE if team == PieceTeam.BLACK else PieceTeam.BLACK

    # oking stands for "Opposing Team's King".
    squares_the_oking_cant_be_in = engine.get_every_square_the_king_cant_be_in(opposing_team)
    oking_x, oking_y = engine.find_king_pos(opposing_team)

    piece_value_dict = {
        PieceName.PAWN  : 1,
        PieceName.KNIGHT: 2,
        PieceName.BISHOP: 3,
        PieceName.ROOK  : 5,
        PieceName.QUEEN : 9,
        None            : 0,
    }

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

    engine.get_king_status(opposing_team)
    if engine.in_check == opposing_team:
        return 500

    score += piece_value_dict[eaten_piece]
    score += len(engine.pinned_pieces)

    return score
