from connectfoursolve.connectfour import ConnectFour, Heuristic
from connectfoursolve.database import DatabaseConnection
from connectfoursolve.search import AlphaBeta
from connectfoursolve.searchnode import SearchNode

def do_alphabeta(db):
	initial_node = SearchNode(ConnectFour())
	alphabeta = AlphaBeta(db_connection=db)
	depth = 8
	for child_node in initial_node.get_successors():
		value = alphabeta.alphabeta(child_node, depth-1, False)
		print("Child node:")
		print(child_node.cf.to_human_readable_string())
		print("Value:", value)

def count_unique_states_at_each_depth(db):
	state_to_cf_prev_depth = {}
	state_to_cf = {}
	depth = None
	for row in db.get_fringe():
		state = row[0]
		depth = row[1]+1
		state_to_cf_prev_depth[state] = ConnectFour.create_from_string(state)
	if depth is None:
		depth = 0
	else:
		print("Fetched fringe from database. Depth={d} States={s}".format(
			d=depth-1, s=len(state_to_cf_prev_depth)))
	while depth <= 10:
		n_states = 0
		if depth == 0:
			cf = ConnectFour()
			state_to_cf = {cf.to_string(): cf}
		else:
			for cf in state_to_cf_prev_depth.values():
				for cf_successor in [x.cf for x in SearchNode(cf).get_successors()]:
					n_states += 1
					state = cf_successor.to_string()
					state_to_cf[state] = cf_successor
		n_solved_states = 0
		for (state, cf) in state_to_cf.items():
			if abs(cf.get_heuristic_value()) >= Heuristic.heuristic_value_win_threshold:
				n_solved_states += 1
				db.set_value_of_state(state, cf.get_heuristic_value())
		print("Depth {d} States: {s:,} Unique states: {us:,} ({ss:,} solved) ({max:,} max)".format(
			d=depth, s=n_states, us=len(state_to_cf), ss=n_solved_states, max=7**depth))
		unsolved_states = [
			state for (state, cf) in state_to_cf.items()
			if abs(cf.get_heuristic_value()) < Heuristic.heuristic_value_win_threshold
		]
		db.add_fringe(unsolved_states, depth)
		state_to_cf_prev_depth = state_to_cf
		state_to_cf = {}
		depth += 1

def print_database(db_connection):
	cursor = db_connection.cursor()
	cursor.execute("select * from connectfour")
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
	#db.execute_sql("delete from connectfour")
	
	print("Number of solved states: ", db.get_number_of_solved_states())
	do_alphabeta(db)
	#count_unique_states_at_each_depth(db)
	print("Number of solved states: ", db.get_number_of_solved_states())
	#print_database(db)
