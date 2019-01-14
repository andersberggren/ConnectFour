from connectfoursolve.connectfour import ConnectFour

class Heuristic:
	"""
	Base class for heuristic value calculations.
	"""
	
	heuristic_value_win_threshold = 1000000
	
	def __init__(self, connect_four):
		self.cf = connect_four
	
	def get_heuristic_value(self):
		return 0
	
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
