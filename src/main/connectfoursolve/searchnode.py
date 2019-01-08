from connectfoursolve.connectfour import ConnectFour

class SearchNode:
	def __init__(self, cf):
		self.cf = cf
	
	def get_successors(self):
		successors = []
		for i in range(ConnectFour.width):
			successor_cf = ConnectFour(self.cf)
			try:
				successor_cf.place_disc(i)
				successors.append(SearchNode(successor_cf))
			except ValueError:
				pass
		return successors
