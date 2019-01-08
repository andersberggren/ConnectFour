class ConnectFour:
	symbols = ["X", "O"]
	width = 7
	height = 6
	
	def __init__(self, parent=None):
		self.position_to_disc = {} if parent is None else dict(parent.position_to_disc) 
	
	def place_disc(self, column):
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
			winner = self.get_winner_one_direction(x, 0, (0,1))
			if winner is not None:
				return winner
		# Horizontal
		for y in range(ConnectFour.width):
			winner = self.get_winner_one_direction(0, y, (1,0))
			if winner is not None:
				return winner
		# Diagonal /
		for x in range(4-ConnectFour.height, ConnectFour.width+1-4):
			winner = self.get_winner_one_direction(x, 0, (1,1))
			if winner is not None:
				print("Diagonal win! /")
				return winner
		for x in range(4-ConnectFour.height, ConnectFour.width+1-4):
			winner = self.get_winner_one_direction(x, ConnectFour.height-1, (1,-1))
			if winner is not None:
				print("Diagonal win! \\")
				return winner
		return None
	
	def get_winner_one_direction(self, x_start, y_start, direction):
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
	
	def get_state_as_string(self):
		s = ""
		for y in range(ConnectFour.height):
			for x in range(ConnectFour.width):
				try:
					s += ConnectFour.symbols[self.position_to_disc[(x,y)]]
				except KeyError:
					s += "."
		return s