from connectfoursolve.connectfour import ConnectFour

class SearchNode:
	def __init__(self, cf):
		self.cf = cf
	
	def get_successors(self):
		if self.cf.get_winner() is not None:
			return []
		successors = []
		for i in range(ConnectFour.width):
			try:
				successor_cf = ConnectFour(self.cf, i)
				successors.append(SearchNode(successor_cf))
			except ValueError:
				pass
		return successors
