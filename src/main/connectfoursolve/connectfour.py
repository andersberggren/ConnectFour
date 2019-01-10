class ConnectFour:
	width = 7
	height = 6
	
	def __init__(self, parent=None):
		self.discs = [[None] * ConnectFour.height for x in range(ConnectFour.width)]
		if parent is not None:
			for x in range(ConnectFour.width):
				for y in range(ConnectFour.height):
					self.discs[x][y] = parent.discs[x][y]
		self.heuristic = Heuristic(self)
		self.heuristic_value = None
	
	def place_disc(self, column):
		if column < 0 or column >= ConnectFour.width:
			raise ValueError("Invalid column: {}".format(column))
		for row in range(ConnectFour.height):
			if self.discs[column][row] is None:
				self.discs[column][row] = self.get_current_player()
				return True
		return False
	
	def get_number_of_discs(self):
		count = 0
		for x in range(7):
			for y in range(6):
				if self.discs[x][y] is not None:
					count += 1
		return count
		#return len([disc for column in self.discs for disc in column if disc is not None])
	
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
		while x < ConnectFour.width and y < ConnectFour.height:
			try:
				this_player = self.discs[x][y]
				if this_player == player:
					discs_in_a_row += 1
					if discs_in_a_row == 4:
						return player
				else:
					player = this_player
					discs_in_a_row = 1
			except IndexError:
				player = None
				discs_in_a_row = 0
			x += direction[0]
			y += direction[1]
		return None
	
	def get_heuristic_value(self):
		if self.heuristic_value is None:
			self.heuristic_value = self.heuristic.get_heuristic_value()
		return self.heuristic_value
	
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

class Heuristic:
	def __init__(self, connect_four):
		self.cf = connect_four
	
	def get_heuristic_value(self):
		winner = self.cf.get_winner()
		if winner is not None:
			return self.get_heuristic_value_for_win(winner, 0)
		
		player_threat_list = self.get_threats()
		current_player = self.cf.get_current_player()
		opponent = 1 - current_player
		
		# If current player has an immediate threat, current player will win in 1 move.
		if len(player_threat_list[current_player][0]) > 0:
			#print("Current player has an immediate threat. Will win in 1 move.")
			return self.get_heuristic_value_for_win(current_player, 1)
		
		# If opponent has more than one immediate threat, opponent will win in 2 moves.
		opponent_immediate_threats = player_threat_list[opponent][0]
		opponent_threats = player_threat_list[opponent][1]
		if len(opponent_immediate_threats) > 1:
			#print("Opponent has {} immediate threats and will win in 2 moves.".format(
			#		len(opponent_immediate_threats)))
			return self.get_heuristic_value_for_win(opponent, 2)
		
		# If opponent has an immediate and a non-immediate threat in the same column,
		# opponent will win in 2 moves.
		if any(t1 == t2 for t1 in opponent_immediate_threats for t2 in opponent_threats):
			#print("Opponent has both an immediate and a non-immediate threat in the same column.")
			return self.get_heuristic_value_for_win(opponent, 2)
		return 0
	
	def get_heuristic_value_for_win(self, player, number_of_moves_left):
		value = 1000000 + ConnectFour.width*ConnectFour.height \
				- (self.cf.get_number_of_discs()+number_of_moves_left)
		return value if player == 0 else -value
	
	def get_threats(self):
		"""
		Returns a list of:
		  (list_of_columns_with_immediate_threats, list_of_columns_with_threats).
		"""
		(positions_immediate_threat, positions_threat) = self.get_threat_positions()
		player_threat_list = []
		for player in [0, 1]:
			player_immediate_threats = []
			player_threats = []
			for position in positions_immediate_threat:
				if self.is_threat(position, player):
					player_immediate_threats.append(position[0])
			for position in positions_threat:
				if self.is_threat(position, player):
					player_threats.append(position[0])
			player_threat_list.append((player_immediate_threats, player_threats))
		return player_threat_list
	
	def get_threat_positions(self):
		"""
		Returns (list_of_positions_for_immediate_threats, list_of_positions_for_threats).
		"""
		immediate_threats = []
		threats = []
		for x in range(ConnectFour.width):
			position_immediate_threat = None
			position_threat = None
			for y in range(ConnectFour.height):
				position = (x, y)
				if self.cf.discs[x][y] is None:
					if position_immediate_threat is None:
						position_immediate_threat = position
					elif position_threat is None:
						position_threat = position
						break
			if position_immediate_threat is not None:
				immediate_threats.append(position_immediate_threat)
			if position_threat is not None:
				threats.append(position_threat)
		return (immediate_threats, threats)
		
	def is_threat(self, position, player):
		directions = [(0,1), (1,0), (1,1), (1,-1)]
		for direction in directions:
			in_a_row = 1
			(x, y) = (position[0], position[1])
			while True:
				(x, y) = (x+direction[0], y+direction[1])
				try:
					if self.cf.discs[x][y] == player:
						in_a_row += 1
					else:
						break
				except IndexError:
					break
			(x, y) = (position[0], position[1])
			while True:
				(x, y) = (x-direction[0], y-direction[1])
				try:
					if self.cf.discs[x][y] == player:
						in_a_row += 1
					else:
						break
				except IndexError:
					break
			if in_a_row >= 4:
				return True
		return False
