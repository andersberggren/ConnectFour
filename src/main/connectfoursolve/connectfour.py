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

class Heuristic:
	heuristic_value_win_threshold = 1000000
	
	def __init__(self, connect_four):
		self.cf = connect_four
	
	def get_heuristic_value(self):
		winner = self.cf.get_winner()
		if winner is not None:
			return self.get_heuristic_value_for_win(winner, 0)
		if self.cf.get_number_of_discs() == ConnectFour.width * ConnectFour.height:
			return 0
		
		threats = self.get_threats()
		immediate_threats = [self.get_immediate_threats(x) for x in threats]
		current_player = self.cf.get_current_player()
		opponent = (current_player+1) % 2
		
		# If current player has an immediate threat, current player will win in 1 move.
		if len(immediate_threats[current_player]) > 0:
			#print("Current player has an immediate threat. Will win in 1 move.")
			return self.get_heuristic_value_for_win(current_player, 1)
		
		# If opponent has more than one immediate threat, opponent will win in 2 moves.
		if len(immediate_threats[opponent]) > 1:
			#print("Opponent has more than 1 immediate threat and will win in 2 moves.")
			return self.get_heuristic_value_for_win(opponent, 2)
		
		# If opponent has exactly one immediate threat, place a disc in that column,
		# and get heuristic value for that state.
		if len(immediate_threats[opponent]) == 1:
			#print("Opponent has 1 immediate threat. Return the heuristic value of the " \
			#		+ "state resulting from placing a disc in that column.")
			cf_successor = ConnectFour(self.cf)
			column_of_threat = next(iter(immediate_threats[opponent]))[0]
			cf_successor.place_disc(column_of_threat)
			return cf_successor.get_heuristic_value()
		
		if all(len(x) == 0 for x in threats):
			# Neither player has any threats.
			# Player with the most central discs has advantage.
			return sum([
				abs(ConnectFour.width//2 - x) * (-1 if self.cf.discs[x][y] == 0 else 1)
				for x in range(ConnectFour.width) for y in range(ConnectFour.height)
				if self.cf.discs[x][y] is not None
			])
		
		# Determine which player has advantage, based on zugzwang.
		# Which positions are playable for both players?
		# Take turns and place disc in those positions as long as possible.
		# After that, it's either:
		# - Player has to play a disc where opponent has an active threat (and loses)
		# - Player has to sacrifice own threat
		open_positions = self.get_open_positions()
		while True:
			if len(open_positions) == 0:
				return 100 * (len(threats[0]) - len(threats[1]))
			playable_positions = []
			for player in [0, 1]:
				playable_positions.append({
					(x,y) for (x,y) in open_positions
					if (y == 0 or (x,y-1) not in open_positions) \
							and (x,y+1) not in threats[(player+1)%2]
				})
			if len(playable_positions[current_player]) == 0:
				return 1000 * (-1 if current_player == 0 else 1)
			playable_positions_common = playable_positions[0] & playable_positions[1]
			if len(playable_positions_common) > 1:
				open_positions.remove(playable_positions_common.pop())
				current_player = (current_player+1) % 2
				continue
			# Current player has to sacrifice own threat.
			# Look for position that changes zugzwang.
			zugswang_position = next((
				(x,y) for (x,y) in playable_positions[current_player]
				if (ConnectFour.height-y) % 2 == 0
			), None)
			if zugswang_position is not None:
				open_positions.remove(zugswang_position)
				current_player = (current_player+1) % 2
				continue
			open_positions.remove(playable_positions[current_player].pop())
			current_player = (current_player+1) % 2
	
	def get_heuristic_value_for_win(self, player, number_of_moves_left):
		value = 1000000 + ConnectFour.width*ConnectFour.height \
				- (self.cf.get_number_of_discs()+number_of_moves_left)
		return value if player == 0 else -value
	
	def get_open_positions(self):
		return {
			(x,y) for x in range(ConnectFour.width) for y in range(ConnectFour.height)
			if self.cf.discs[x][y] is None
		}
		
	def get_immediate_threats(self, threats):
		immediate_threats = set()
		for threat in sorted(threats, key=lambda pos: (pos[1],pos[0])):
			if threat[1] == 0 or self.cf.discs[threat[0]][threat[1]-1] is not None \
					or (threat[0], threat[1]-1) in immediate_threats:
				immediate_threats.add(threat)
		return immediate_threats
	
	def get_threats(self):
		"""
		Returns a list of lists with player threats.
		"""
		player_threat_list = []
		open_positions = self.get_open_positions()
		for player in [0, 1]:
			player_threats = []
			for position in open_positions:
				if self.is_threat(position, player):
					player_threats.append(position)
			player_threat_list.append(player_threats)
		return player_threat_list
	
	def is_threat(self, position, player):
		"""
		Returns True iff player "player" would win by placing a disc at position "position".
		"""
		directions = [(0,1), (1,0), (1,1), (1,-1)]
		for direction in directions:
			in_a_row = 1
			(x, y) = (position[0], position[1])
			while True:
				(x, y) = (x+direction[0], y+direction[1])
				if x < 0 or x >= ConnectFour.width or y < 0 or y >= ConnectFour.height:
					break
				if self.cf.discs[x][y] == player:
					in_a_row += 1
				else:
					break
			(x, y) = (position[0], position[1])
			while True:
				(x, y) = (x-direction[0], y-direction[1])
				if x < 0 or x >= ConnectFour.width or y < 0 or y >= ConnectFour.height:
					break
				if self.cf.discs[x][y] == player:
					in_a_row += 1
				else:
					break
			if in_a_row >= 4:
				return True
		return False
