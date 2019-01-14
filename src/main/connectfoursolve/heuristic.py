from connectfoursolve.connectfour import ConnectFour

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
			return Heuristic(cf_successor).get_heuristic_value()
		
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
		value = Heuristic.heuristic_value_win_threshold + ConnectFour.width*ConnectFour.height \
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
