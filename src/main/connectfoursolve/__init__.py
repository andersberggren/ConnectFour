from connectfoursolve.connectfour import ConnectFour, Heuristic
from connectfoursolve.db import connect_to_db, get_value_of_state, set_value_of_state, get_number_of_rows
from connectfoursolve.search import AlphaBeta
from connectfoursolve.searchnode import SearchNode

def do_alphabeta(db_connection):
	initial_node = SearchNode(ConnectFour())
	alphabeta = AlphaBeta(db_connection=db_connection)
	for child_node in initial_node.get_successors():
		value = alphabeta.alphabeta(child_node, 7, False)
		print("Child node:")
		print(child_node.cf.to_human_readable_string())
		print("Value:", value)

def print_database(db_connection):
	cursor = db_connection.cursor()
	cursor.execute("select * from connectfour")
	#cursor.execute("select distinct value from connectfour order by value")
	i = 0
	for (state, value, move) in cursor:
		print("Row:", i, "State:", state, "Value:", value)
		cf = ConnectFour()
		for x in range(ConnectFour.width):
			column_as_hex_string = state[x*2:x*2+2]
			column_as_bin_string = bin(int(column_as_hex_string, 16))[2:]
			for y in range(len(column_as_bin_string)-1):
				player = int(column_as_bin_string[-1-y])
				cf.position_to_disc[(x,y)] = player
		print(cf.to_human_readable_string())
		i += 1
		if i == 100:
			break

def count_unique_states_at_each_depth(db_connection):
	state_to_cf_prev_depth = {}
	state_to_cf = {}
	depth = 0
	while depth <= 8:
		if depth == 0:
			cf = ConnectFour()
			state_to_cf = {cf.to_string(): cf}
		else:
			for cf in state_to_cf_prev_depth.values():
				for cf_successor in [x.cf for x in SearchNode(cf).get_successors()]:
					state = cf_successor.to_string()
					state_to_cf[state] = cf_successor
		n_solved_states = 0
		for (state, cf) in state_to_cf.items():
			if cf.get_heuristic_value() >= Heuristic.heuristic_value_win_threshold:
				n_solved_states += 1
				if get_value_of_state(db_connection, state) is None:
					set_value_of_state(db_connection, state, cf.get_heuristic_value(), -1)
		print("Depth {d} Unique states: {us} ({ss} solved) ({max} max)".format(
			d=depth, us=len(state_to_cf), ss=n_solved_states, max=7**depth))
		state_to_cf_prev_depth = state_to_cf
		state_to_cf = {}
		depth += 1

if __name__ == "__main__":
	db_connection = connect_to_db()
	#db_connection.cursor().execute("delete from connectfour")
	#db_connection.commit()
	print("Number of rows in connectfour: ", get_number_of_rows(db_connection))
	#do_alphabeta(db_connection)
	count_unique_states_at_each_depth(db_connection)
	print("Number of rows in connectfour: ", get_number_of_rows(db_connection))
	#print_database(db_connection)
