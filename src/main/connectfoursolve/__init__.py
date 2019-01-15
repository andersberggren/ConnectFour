from connectfoursolve.connectfour import ConnectFour
from connectfoursolve.database import DatabaseConnection
from connectfoursolve.search import AlphaBeta
from connectfoursolve.searchnode import SearchNode
from connectfoursolve.heuristic import Heuristic
from connectfoursolve.heuristic100 import Heuristic100

def do_alphabeta(db):
	initial_node = SearchNode(ConnectFour(), Heuristic100)
	alphabeta = AlphaBeta(db_connection=db)
	depth = 8
	for child_node in initial_node.get_successors():
		value = alphabeta.alphabeta(child_node, depth-1, False)
		print("Child node:")
		print(child_node.cf.to_human_readable_string())
		print("Value:", value)

def count_unique_states_at_each_depth(db):
	heuristic_class = Heuristic100
	state_to_node_prev_depth = {}
	state_to_node = {}
	depth = None
	for row in db.get_fringe():
		state = row[0]
		depth = row[1]+1
		cf = ConnectFour.create_from_string(state)
		node = SearchNode(cf, heuristic_class)
		state_to_node_prev_depth[state] = node
	if depth is None:
		depth = 0
	else:
		print("Fetched fringe from database. Depth={d} States={s}".format(
			d=depth-1, s=len(state_to_node_prev_depth)))
	while depth <= 6:
		n_states = 0
		if depth == 0:
			node = SearchNode(ConnectFour(), heuristic_class)
			state_to_node = {node.get_state(): node}
		else:
			for node in state_to_node_prev_depth.values():
				for successor in node.get_successors():
					n_states += 1
					state = successor.get_state()
					state_to_node[state] = successor
		n_solved_states = 0
		for (state, node) in state_to_node.items():
			if abs(node.get_heuristic_value()) >= Heuristic.heuristic_value_win_threshold:
				n_solved_states += 1
				db.set_value_of_state(state, node.get_heuristic_value())
		print("Depth {d} States: {s:,} Unique states: {us:,} ({ss:,} solved) ({max:,} max)".format(
			d=depth, s=n_states, us=len(state_to_node), ss=n_solved_states, max=7**depth))
		unsolved_states = [
			state for (state, node) in state_to_node.items()
			if abs(node.get_heuristic_value()) < Heuristic.heuristic_value_win_threshold
		]
		db.add_fringe(unsolved_states, depth)
		state_to_node_prev_depth = state_to_node
		state_to_node = {}
		depth += 1

def print_database(db):
	cursor = db.execute_sql("select * from connectfour")
	i = 0
	for (state, value, move) in cursor:  # @UnusedVariable
		print("Row:", i, "State:", state, "Value:", value)
		cf = ConnectFour.create_from_string(state)
		print(cf.to_human_readable_string())
		i += 1
		if i == 1000:
			break

if __name__ == "__main__":
	db = DatabaseConnection()
	#db.execute_sql_and_commit("delete from connectfour")
	
	print("Number of solved states: ", db.get_number_of_solved_states())
	do_alphabeta(db)
	#count_unique_states_at_each_depth(db)
	print("Number of solved states: ", db.get_number_of_solved_states())
	#print_database(db)
