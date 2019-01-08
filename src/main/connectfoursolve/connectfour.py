class ConnectFour:
	width = 7
	height = 6
	
	def __init__(self, parent=None, move=None):
		self.position_to_disc = {} if parent is None else dict(parent.position_to_disc)
		self.move = move
		if self.move is not None:
			self.place_disc(self.move)
	
	def place_disc(self, column):
		if column < 0 or column >= ConnectFour.width:
			raise ValueError("Invalid column: {}".format(column))
		row_index = 0
		while (column, row_index) in self.position_to_disc:
			row_index += 1
		if row_index < ConnectFour.height:
			self.position_to_disc[(column, row_index)] = self.get_current_player()
		else:
			raise ValueError("Can't place a disc in column {}. It is full.".format(column))
	
	def get_current_player(self):
		return len(self.position_to_disc) % 2
	
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
		while x < ConnectFour.width and y < ConnectFour.height:
			try:
				this_player = self.position_to_disc[(x,y)]
				if this_player == player:
					discs_in_a_row += 1
					if discs_in_a_row == 4:
						return player
				else:
					player = this_player
					discs_in_a_row = 1
			except KeyError:
				player = None
				discs_in_a_row = 0
			x += direction[0]
			y += direction[1]
		return None
	
	def get_heuristic_value(self):
		winner = self.get_winner()
		if winner is not None:
			value = 1000000 + ConnectFour.width*ConnectFour.height - len(self.position_to_disc)
			return value if winner == 0 else -value
		else:
			return 0
	
	def get_state_as_string(self):
		symbols = ["X", "O"]
		s = ""
		for y in range(ConnectFour.height-1, -1, -1):
			for x in range(ConnectFour.width):
				try:
					s += symbols[self.position_to_disc[(x,y)]]
				except KeyError:
					s += "."
		return s
