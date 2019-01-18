# A node in alphabeta search needs the following methods:
# - is_solved()  Returns True iff the node represents a terminal state, or the node is solved
#                (i.e. it can determine the outcome from optimal play)
# - get_heuristic_value()
# - get_successors()
# - get_state() Returns a string representation of the node. Used when writing to database.
class AlphaBeta:
	def __init__(self, db_connection=None):
		self.db = db_connection
		self.number_of_db_writes = 0
		self.n_created_nodes = 0
		self.n_evaluated_nodes = 0
	
	def alphabeta(self, node, depth, maximizing_player, alpha=None, beta=None):
		self.n_evaluated_nodes += 1
		value_from_db = self.get_heuristic_value_from_database(node)
		if value_from_db is not None:
			return (node, value_from_db)
		heuristic_value = node.get_heuristic_value()
		if node.is_solved():
			self.set_heuristic_value(node, heuristic_value)
			return (node, heuristic_value)
		if depth == 0:
			return (node, heuristic_value)
		
		best_child_node = None
		best_child_value = None
		successors = node.get_successors()
		self.n_created_nodes += len(successors)
		for child_node in successors:
			(_, child_value) = self.alphabeta(child_node, depth-1, not maximizing_player, alpha, beta)
			if maximizing_player:
				if child_value is not None and (best_child_value is None or child_value > best_child_value):
					best_child_value = child_value
					best_child_node = child_node
					if alpha is None or best_child_value > alpha:
						alpha = best_child_value
			else:
				if child_value is not None and (best_child_value is None or child_value < best_child_value):
					best_child_value = child_value
					best_child_node = child_node
					if beta is None or best_child_value < beta:
						beta = best_child_value
			if alpha is not None and beta is not None and alpha >= beta:
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
