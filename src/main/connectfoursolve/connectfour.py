class ConnectFour:
	width = 7
	height = 6
	
	def __init__(self, parent=None):
		self.discs = [[None] * ConnectFour.height for x in range(ConnectFour.width)]
		if parent is not None:
			for x in range(ConnectFour.width):
				for y in range(ConnectFour.height):
					self.discs[x][y] = parent.discs[x][y]
	
	def place_disc(self, column):
		if column < 0 or column >= ConnectFour.width:
			raise ValueError("Invalid column: {}".format(column))
		for row in range(ConnectFour.height):
			if self.discs[column][row] is None:
				self.discs[column][row] = self.get_current_player()
				return True
		return False
	
	def get_number_of_discs(self):
		return len([
			1 for x in range(ConnectFour.width) for y in range(ConnectFour.height)
			if self.discs[x][y] is not None
		])
	
	def get_current_player(self):
		return self.get_number_of_discs() % 2
	
	def get_winner(self):
		# Vertical
		for x in range(ConnectFour.height):
			winner = self._get_winner_one_direction(x, 0, (0,1))
			if winner is not None:
				return winner
		# Horizontal
		for y in range(ConnectFour.width):
			winner = self._get_winner_one_direction(0, y, (1,0))
			if winner is not None:
				return winner
		# Diagonal /
		for x in range(4-ConnectFour.height, ConnectFour.width+1-4):
			winner = self._get_winner_one_direction(x, 0, (1,1))
			if winner is not None:
				return winner
		# Diagonal \
		for x in range(4-ConnectFour.height, ConnectFour.width+1-4):
			winner = self._get_winner_one_direction(x, ConnectFour.height-1, (1,-1))
			if winner is not None:
				return winner
		return None
	
	def _get_winner_one_direction(self, x_start, y_start, direction):
		x = x_start
		y = y_start
		player = None
		discs_in_a_row = 0
		while not (x < 0 and direction[0] < 0) \
				and not (x >= ConnectFour.width and direction[0] > 0) \
				and not (y < 0 and direction[1] < 0) \
				and not (y >= ConnectFour.height and direction[1] > 0):
			if x >= 0 and x < ConnectFour.width and y >= 0 and y < ConnectFour.height:
				this_player = self.discs[x][y]
				if this_player is None:
					player = None
					discs_in_a_row = 0
				elif this_player == player:
					discs_in_a_row += 1
					if discs_in_a_row == 4:
						return player
				else:
					player = this_player
					discs_in_a_row = 1
			x += direction[0]
			y += direction[1]
		return None
	
	def is_game_over(self):
		return self.get_number_of_discs() == ConnectFour.width*ConnectFour.height \
				or self.get_winner() is not None
	
	def to_string(self):
		column_strings = []
		for x in range(ConnectFour.width):
			column_height = 0
			column_value = 0
			for y in range(ConnectFour.height-1, -1, -1):
				disc_value = self.discs[x][y]
				if disc_value is not None:
					column_height = max(column_height, y+1)
					column_value = (column_value<<1) + disc_value
			column_value += 1<<column_height
			column_strings.append("{0:02x}".format(column_value))
		cf_string = "".join(column_strings)
		cf_mirrored_string = "".join([x for x in reversed(column_strings)])
		return min(cf_string, cf_mirrored_string)
	
	def to_human_readable_string(self):
		player_to_symbol = {0: "X", 1: "O"}
		s = ""
		for y in range(ConnectFour.height-1, -1, -1):
			for x in range(ConnectFour.width):
				symbol = "."
				try:
					symbol = player_to_symbol[self.discs[x][y]]
				except KeyError:
					pass
				s += symbol
			s += "\n"
		s = s.rstrip()
		return s
	
	@staticmethod
	def create_from_string(state):
		cf = ConnectFour()
		for x in range(ConnectFour.width):
			column_as_hex_string = state[x*2:x*2+2]
			column_as_bin_string = bin(int(column_as_hex_string, 16))[2:]
			for y in range(len(column_as_bin_string)-1):
				player = int(column_as_bin_string[-1-y])
				cf.discs[x][y] = player
		return cf
