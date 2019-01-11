from connectfoursolve.connectfour import ConnectFour, Heuristic
from connectfoursolve.db import connect_to_db, get_value_of_state, set_value_of_state, \
                                get_number_of_rows, add_fringe, get_fringe
from connectfoursolve.search import AlphaBeta
from connectfoursolve.searchnode import SearchNode

def do_alphabeta(db_connection):
	initial_node = SearchNode(ConnectFour())
	alphabeta = AlphaBeta(db_connection=db_connection)
	for child_node in initial_node.get_successors():
		value = alphabeta.alphabeta(child_node, 42, False)
		print("Child node:")
		print(child_node.cf.to_human_readable_string())
		print("Value:", value)

def count_unique_states_at_each_depth(db_connection):
	state_to_cf_prev_depth = {}
	state_to_cf = {}
	depth = None
	cursor = get_fringe(db_connection)
	for row in cursor:
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
				set_value_of_state(db_connection, state, cf.get_heuristic_value())
		print("Depth {d} States: {s:,} Unique states: {us:,} ({ss:,} solved) ({max:,} max)".format(
			d=depth, s=n_states, us=len(state_to_cf), ss=n_solved_states, max=7**depth))
		unsolved_states = [
			state for (state, cf) in state_to_cf.items()
			if abs(cf.get_heuristic_value()) < Heuristic.heuristic_value_win_threshold
		]
		add_fringe(db_connection, unsolved_states, depth)
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
	db_connection = connect_to_db()
	#db_connection.cursor().execute("delete from connectfour")
	#db_connection.commit()
	
	#cf = ConnectFour.create_from_string("010b0703010404")
	#print(cf.to_human_readable_string())
	#print(cf.get_heuristic_value())
	
	print("Number of rows in connectfour: ", get_number_of_rows(db_connection))
	do_alphabeta(db_connection)
	#count_unique_states_at_each_depth(db_connection)
	print("Number of rows in connectfour: ", get_number_of_rows(db_connection))
	#print_database(db_connection)
