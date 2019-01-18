from connectfoursolve.connectfour import ConnectFour
from connectfoursolve.heuristic import Heuristic

class SearchNode:
	def __init__(self, cf, heuristic_class):
		self.cf = cf
		self.heuristic_class = heuristic_class
		self.heuristic_value = None
	
	def is_solved(self):
		return abs(self.get_heuristic_value()) >= Heuristic.heuristic_value_win_threshold \
				or self.cf.is_game_over()
	
	def get_heuristic_value(self):
		if self.heuristic_value is None:
			self.heuristic_value = self.heuristic_class(self.cf).get_heuristic_value()
		return self.heuristic_value
	
	def get_successors(self):
		if self.cf.get_winner() is not None:
			return []
		successors = []
		for i in range(ConnectFour.width):
			successor_cf = ConnectFour(self.cf)
			if successor_cf.place_disc(i):
				successors.append(SearchNode(successor_cf, self.heuristic_class))
		successors.sort(
			key=lambda x: x.get_heuristic_value(),
			reverse=self.cf.get_current_player() == 0
		)
		return successors
	
	def get_state(self):
		return self.cf.to_string()
