from connectfoursolve.heuristic import Heuristic

alpha_default = -1000000000
beta_default  =  1000000000

# SearchNode needs the following methods:
# - is_terminal_node()
# - get_heuristic_value()
# - get_successors()
# - get_state() Optional, to prevent creation/evaluation of equivalent nodes
class AlphaBeta:
	def __init__(self, db_connection=None):
		self.db = db_connection
		self.number_of_db_writes = 0
		self.n_created_nodes = 0
		self.n_evaluated_nodes = 0
	
	def alphabeta(self, node, depth, maximizing_player, alpha=alpha_default, beta=beta_default):
		self.n_evaluated_nodes += 1
		value_from_db = self.get_heuristic_value_from_database(node)
		if value_from_db is not None:
			return (node, value_from_db)
		heuristic_value = node.get_heuristic_value()
		if abs(heuristic_value) >= Heuristic.heuristic_value_win_threshold \
				or node.is_terminal_node():
			self.set_heuristic_value(node, heuristic_value)
			return (node, heuristic_value)
		if depth == 0:
			return (node, heuristic_value)
		
		best_child_node = None
		best_child_value = alpha_default if maximizing_player else beta_default
		successors = node.get_successors()
		self.n_created_nodes += len(successors)
		for child_node in successors:
			child_state = child_node.get_state()
			(_, child_value) = self.alphabeta(child_node, depth-1, not maximizing_player, alpha, beta)
			if maximizing_player:
				if child_value > best_child_value:
					best_child_value = child_value
					best_child_node = child_node
				alpha = max(alpha, best_child_value)
			else:
				if child_value < best_child_value:
					best_child_value = child_value
					best_child_node = child_node
				beta = min(beta, best_child_value)
			if alpha >= beta:
				break
		return (best_child_node, best_child_value)
	
	def get_heuristic_value_from_database(self, node):
		if self.db is None:
			return None
		return self.db.get_value_of_state(node.cf.to_string())
	
	def set_heuristic_value(self, node, value):
		if self.db is None:
			return
		self.db.set_value_of_state(node.get_state(), value)
		self.number_of_db_writes += 1
		if self.number_of_db_writes % 1000 == 0:
			print("{} states written to database".format(self.number_of_db_writes))
			print("{} skipped nodes".format(self.n_skipped_states))
