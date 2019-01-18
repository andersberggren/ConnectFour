from connectfoursolve.heuristic import Heuristic

class Heuristic1(Heuristic):
	def get_heuristic_value(self):
		winner = self.cf.get_winner()
		if winner is not None:
			return self.get_heuristic_value_for_win(winner)
		else:
			return 0
