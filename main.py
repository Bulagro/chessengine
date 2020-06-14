from Enum import enum, auto

# This singleton must be moved to a file so it can stop being a class.
class Board:
	def set_pieces(self):
		self.pieces = [[]]

	def is_square_empty(pos: Pos):
		if pos.x < 0 or pos.x > 7 or pos.y < 0 or pos.y > 7:
			return None

		for p in self.pieces:
			if pos == p.pos:
				return True
		return False

	def get_piece(pos: Pos):
		if is_square_empty(pos) == False:
			return self.pieces[pos.x][pos.y].get()

Board = Board()

class Team(enum):
	WHITE = auto()
	BLACK = auto()

class Pos:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

	def is_in_line(self, other: Pos):
		return self.x == other.x or self.y == other.y
	
	# Delete if not used
	def is_in_board(self, other: Pos):
		return not pos.x < 0 or pos.x > 7 or pos.y < 0 or pos.y > 7

	def get_offset(self, x: int, y: int):
		return Pos(self.x + x, self.y + y)
	
	def __eq__(self, other: Pos):
		return self.x == other.x and self.y == other.y

class Piece:
	def __init__(pos: Pos, team: Team):
		self.pos = pos
		self.team = team
		self.pinned = False

	def get(self):
		return (self.team, type(self))

	def _check_move(self, pos: Pos):
		return False

class Pawn(Piece):
	def __init__(self, pos: Pos, team: Team):
		super.__init__(pos, team)
		self.has_moved = False
		self.fwd = 1 if team == Team().WHITE else -1

	def get_moves(self):
		moves = []

		if not has_moved and Board.is_square_empty(self.pos.get_offset(2 * fwd, 0)):
			moves.append(self.pos.get_offset(2 * fwd, 0))

		if Board.is_square_empty(self.pos.get_offset(1 * fwd, 0))
			moves.append(self.pos.get_offset(1 * fwd, 0))

		# Add attacking moves.

class Knight(Piece):
	def __init__(self, pos: Pos, team: Team):
		super.__init__(pos, team)

	def get_moves(self):
		pass
