from connectfoursolve.connectfour import ConnectFour

class SearchNode:
	def __init__(self, cf):
		self.cf = cf
	
	def is_terminal_node(self):
		return self.cf.get_winner() is not None \
				or self.cf.get_number_of_discs() == ConnectFour.width*ConnectFour.height
	
	def get_heuristic_value(self):
		return self.cf.get_heuristic_value()
	
	def get_successors(self):
		if self.cf.get_winner() is not None:
			return []
		successors = []
		for i in range(ConnectFour.width):
			successor_cf = ConnectFour(self.cf)
			if successor_cf.place_disc(i):
				successors.append(SearchNode(successor_cf))
		return successors
	
	def get_state(self):
		return self.cf.to_string()
