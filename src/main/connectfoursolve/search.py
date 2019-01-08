import connectfoursolve
from connectfoursolve.db import get_value_of_state

alpha_default = -1000000000
beta_default  =  1000000000

# SearchNode needs the following methods:
# - is_terminal_node()
# - get_heuristic_value()
# - get_successors()
# - get_state() Optional, to prevent creation/evaluation of equivalent nodes
class AlphaBeta:
	def __init__(self, db_connection=None):
		self.node_state_to_heuristic_value = {}
		self.n_terminal_nodes = 0
		self.db_connection = db_connection
	
	def alphabeta(self, node, depth, maximizing_player, alpha=alpha_default, beta=beta_default):
		value_from_db = self.get_heuristic_value_from_database(node)
		if value_from_db is not None:
			print("Returning heuristic value from database:", value_from_db)
			return value_from_db
		if node.is_terminal_node():
			node_state = node.get_state()
			value = node.get_heuristic_value()
			self.node_state_to_heuristic_value[node_state] = value
			self.n_terminal_nodes += 1
			return value
		if depth == 0:
			return node.get_heuristic_value()
		if maximizing_player:
			value = alpha_default
			for child_node in node.get_successors():
				child_value = self.alphabeta(child_node, depth-1, False, alpha, beta)
				if abs(child_value) >= 1000000:
					child_node_state = child_node.get_state()
					self.node_state_to_heuristic_value[child_node_state] = child_value
				value = max(value, child_value)
				alpha = max(alpha, value)
				if alpha >= beta:
					break
		else:
			value = beta_default
			for child_node in node.get_successors():
				child_value = self.alphabeta(child_node, depth-1, True, alpha, beta)
				if abs(child_value) >= 1000000:
					child_node_state = child_node.get_state()
					self.node_state_to_heuristic_value[child_node_state] = child_value
				value = min(value, child_value)
				alpha = min(alpha, value)
				if alpha >= beta:
					break
		return value
	
	def get_heuristic_value_from_database(self, node):
		if self.db_connection is None:
			return None
		return get_value_of_state(self.db_connection, node.cf.get_state_as_string())
