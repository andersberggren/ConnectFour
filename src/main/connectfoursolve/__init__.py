from connectfoursolve.connectfour import ConnectFour
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
	#print("Terminal nodes:", alphabeta.n_terminal_nodes)
	#print("Unique:", len(alphabeta.node_state_to_heuristic_value))
	#for (state, value) in alphabeta.node_state_to_heuristic_value.items():
	#	if get_value_of_state(db_connection, state) is None:
	#		set_value_of_state(db_connection, state, value, -1)

if __name__ == "__main__":
	db_connection = connect_to_db()
	#db_connection.cursor().execute("delete from connectfour")
	#db_connection.commit()
	print("Number of rows in connectfour: ", get_number_of_rows(db_connection))
	do_alphabeta(db_connection)
	print("Number of rows in connectfour: ", get_number_of_rows(db_connection))
