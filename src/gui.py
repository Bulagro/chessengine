from browser import document, window, timer
from browser.html import TABLE, TR, TH, TD, DIV, IMG


C = Chess()
selected_square = -1
possible_moves = []

MAX_STEPS = 20

turn = PieceTeam.WHITE
can_move = True

def is_white(x: int, y: int):
    return (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 != 0)


def click(square: str):
    global selected_square, possible_moves, turn, can_move

    if not can_move:
        return None

    square = int(square)

    if selected_square == -1:
        selected_square = square
        document[str(selected_square)].style.backgroundColor = '#49f540' if is_white(square % 8, square // 8) else '#257a21'

        x, y = selected_square % 8, selected_square // 8
        piece = C.get_piece(x, y)

        if p != EMPTY_SQUARE and piece[1] == turn:
            moves = C.get_piece_moves(x, y, consider_pins=True)
            create_moving_piece(selected_square)

            for x, y in moves:
                _id = str((y * 8) + x)
                possible_moves.append(_id)
                document[_id].style.backgroundColor = '#49f540' if is_white(x, y) else '#257a21'
        else:
            document[str(selected_square)].style.backgroundColor = 'white' if is_white(selected_square % 8, selected_square // 8) else 'black'
            selected_square = -1
            return None

    elif selected_square != -1:
        document[str(selected_square)].style.backgroundColor = '#49f540' if is_white(selected_square % 8, selected_square // 8) else '#257a21'

        if selected_square == square or str(square) not in possible_moves:
            document[str(selected_square)].style.backgroundColor = 'white' if is_white(selected_square % 8, selected_square // 8) else 'black'
            selected_square = -1

            for s in possible_moves:
                s = int(s)
                x, y = s % 8, s // 8
                document[str(s)].style.backgroundColor = 'white' if is_white(x, y) else 'black'

            possible_moves = []
            if 'moving-piece' in document:
                del document['moving-piece']

        elif str(square) in possible_moves:
            ox, oy = int(selected_square) % 8, int(selected_square) // 8
            dx, dy = square % 8, square // 8
            origin_name, origin_team = C.get_piece(ox, oy)
            destiny_name, destiny_team = C.get_piece(dx, dy)

            castle = False
            if origin_name == PieceName.KING and destiny_name == PieceName.ROOK and origin_team == destiny_team:
                castle = True

            castle_y = 0 if origin_team == PieceTeam.BLACK else 7
            pawn_promotion_y = 0 if origin_team == PieceTeam.WHITE else 7
            promotion = dy == pawn_promotion_y and origin_name == PieceName.PAWN

            if origin_name == PieceName.ROOK:
                side = 0 if ox == 0 and oy == castle_y else 1
                C.has_rook_moved[origin_team.value - 1][side] = True

            move_piece(selected_square, str(square), castle, origin_team.name, promotion, destiny_name, destiny_team)

            for s in possible_moves:
                s = int(s)
                x, y = s % 8, s // 8
                document[str(s)].style.backgroundColor = 'white' if is_white(x, y) else 'black'

            possible_moves = []
            document[str(selected_square)].style.backgroundColor = 'white' if is_white(selected_square % 8, selected_square // 8) else 'black'
            selected_square = -1


def get_square(square_id):
    table = list(document['squares'])
    i_square_id = int(square_id)

    x, y = i_square_id % 8, i_square_id // 8
    return list(table[y])[x]


def put_piece_in_square(square_id, name_str, team_str):
    if name_str == 'None':
        get_square(square_id).innerHTML = ''
    else:
        get_square(square_id).innerHTML = f'<img src="static/pieces/{team_str.lower()}_{name_str.lower()}.png">'


def render_board():
    for y in range(8):
        for x in range(8):
            name, team = C.get_piece(x, y)
            if name != None:
                piece_name = name.name
                piece_team = team.name
            else:
                piece_name = 'None'
                piece_team = 'None'

            put_piece_in_square(
                str(y * 8 + x),
                piece_name,
                piece_team,
            )


def create_moving_piece(origin_id):
    origin = get_square(origin_id)
    x = 4 if int(origin_id) % 8 == 0 else 3 # Idk why, but it fixes things.
    y = 2 if int(origin_id) < 8 else 1

    piece_div = DIV(
        id='moving-piece',
        style={
            'left'    : f'{origin.x + x}px',
            'top'     : f'{origin.y + y}px',
            'z-index' : -1,
        }
    )
    piece_div.innerHTML = origin.innerHTML
    document <= piece_div


def move_piece(origin_id, destiny_id, is_castle, team_str, promotion, destiny_name, destiny_team):
    origin = get_square(origin_id)
    destiny = get_square(destiny_id)
    ox = int(origin_id) % 8
    oy = int(origin_id) // 8
    dx = int(destiny_id) % 8
    dy = int(destiny_id) // 8

    put_piece_in_square(origin_id, 'None', 0)

    moving_piece = document['moving-piece']
    moving_piece.style.zIndex = '10'
    moving_piece_img = document['moving-piece'].innerHTML

    def animated_move(timestamp, x_dir, y_dir, step, max_step, castle_dir):
        moving_piece.left += int(x_dir)
        moving_piece.top += int(y_dir)

        if step < max_step:
            timer.request_animation_frame(
                lambda timestamp:
                    animated_move(timestamp, x_dir, y_dir, step + 1, max_step, castle_dir)
            )
        else:
            if castle_dir != 0:
                destiny.innerHTML = ''

                put_piece_in_square(str(int(origin_id + 2 * castle_dir)), 'king', team_str)
                put_piece_in_square(str(int(origin_id) + castle_dir), 'rook', team_str)

                t_value = 0 if team_str == 'WHITE' else 1

                C.has_king_moved[t_value] = True
                C.has_rook_moved[t_value][int(not dx == 0)] = True
            else:
                global can_move, turn
                destiny.innerHTML = moving_piece_img

                if promotion == True: # Display menu for options
                    can_move = False
                    selection_box = DIV(id='piece-select')

                    for name in (PieceName.QUEEN, PieceName.ROOK, PieceName.BISHOP, PieceName.KNIGHT):
                        container = DIV(
                            Class="container",
                            onclick=f'promote_pawn({dx}, {dy}, "{name}", "{team_str}");'
                        )
                        container <= IMG(src=f'static/pieces/{team_str.lower()}_{name.name.lower()}.png')

                        selection_box <= container

                    offset_x = (moving_piece.clientWidth // 2) - (52 * 2)
                    offset_y = -50 if team_str == 'WHITE' else moving_piece.clientWidth

                    selection_box.style.left = str(moving_piece.left + offset_x) + 'px'
                    selection_box.style.top = str(moving_piece.top + offset_y) + 'px'
                    document <= selection_box

            piece_columns = {
                PieceTeam.WHITE : document['rpieces'],
                PieceTeam.BLACK : document['lpieces'],
            }

            if destiny_name != None:
                piece_columns[destiny_team] <= IMG(src=f'static/pieces/{destiny_team.name.lower()}_{destiny_name.name.lower()}.png')

            turn = PieceTeam.BLACK if turn == PieceTeam.WHITE else PieceTeam.WHITE
            display_message()
            del document['moving-piece']

    castle_dir = 0
    if is_castle:
        if dx > ox: castle_dir = 1
        elif ox > dx: castle_dir = -1
        x_dir = (get_square(int(origin_id) + (2 * castle_dir)).x - origin.x) / MAX_STEPS
        y_dir = 0
    else:
        x_dir = (destiny.x - origin.x) / MAX_STEPS
        y_dir = (destiny.y - origin.y) / MAX_STEPS

    timer.request_animation_frame(
        lambda timestamp: animated_move(
            timestamp, x_dir, y_dir, 0, MAX_STEPS, castle_dir
        )
    )

    C.move_piece(ox, oy, dx, dy, is_castle)


def promote_pawn(x: int, y: int, name: PieceName, team_str: str):
    global can_move

    C.replace_piece(x, y, eval(name), eval('PieceTeam.' + team_str))
    put_piece_in_square(str(y * 8 + x), eval(name).name, team_str)

    del document['piece-select']
    can_move = True
    display_message()


def display_message():
    C.get_king_status(turn)

    document['msg'].style.visibility = 'visible'
    can_move = False

    if C.checkmate != None:
        document['msg'].className = 'button'
        document['msg'].bind('click', reset_board)
        document['msg'].text = f'{"BLACK" if turn == PieceTeam.WHITE else "WHITE"} wins!'
    elif C.in_check != None:
        document['msg'].text = f'{turn.name} in check.'
        can_move = True
    elif C.tie == True:
        document['msg'].className = 'button'
        document['msg'].bind('click', reset_board)
        document['msg'].text = 'Tie'
    else:
        document['msg'].style.visibility = 'hidden'
        can_move = True
        document['msg'].unbind('click', reset_board)


def reset_board(event=None):
    global can_move, turn, possible_moves, selected_square

    document['lpieces'].innerHTML = ''
    document['rpieces'].innerHTML = ''
    document['msg'].style.visibility = 'hidden'

    for s in possible_moves:
        s = int(s)
        x, y = s % 8, s // 8
        document[str(s)].style.backgroundColor = 'white' if is_white(x, y) else 'black'

    if str(selected_square) in document:
        document[str(selected_square)].style.backgroundColor = 'white' if is_white(selected_square % 8, selected_square // 8) else 'black'

    selected_square = -1
    possible_moves = []
    turn = PieceTeam.WHITE
    can_move = True

    C.set()
    render_board()


# This is done to have this function usable in js
window.click = click
window.promote_pawn = promote_pawn

####################################################################

# Create table
s = TABLE(id='squares')
p = TABLE(id='pieces')

colors = [(0, 0, 0), (255, 255, 255)]

for row in range(8):
    sr = TR()
    pr = TR()
    color = row % 2 == 0

    for column in range(8):
        _id = str(row*8 + column)

        sr <= TD(
            id=_id,
            style={'background-color' : f'rgb{colors[int(color)]}'}
        )
        pr <= TD(
            id=_id,
            onclick=f"click('{_id}');"
        )
        color = not color

    s <= sr
    p <= pr

document['squares-div'] <= s
document['pieces-div'] <= p

render_board()
