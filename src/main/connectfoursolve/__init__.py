from connectfoursolve.connectfour import ConnectFour
from connectfoursolve.database import DatabaseConnection
from connectfoursolve.heuristic import Heuristic
from connectfoursolve.heuristic100 import Heuristic100
from connectfoursolve.search import AlphaBeta
from connectfoursolve.searchnode import SearchNode
from connectfoursolve.solve import count_unique_states_at_each_depth

def do_alphabeta(db):
	initial_node = SearchNode(ConnectFour(), Heuristic100)
	max_depth = 6
	for depth in range(1, max_depth+1):
		#alphabeta = AlphaBeta(db_connection=db)
		alphabeta = AlphaBeta()
		(node, value) = alphabeta.alphabeta(initial_node, depth, True)
		print("Depth: {d}  Nodes created: {c}  Nodes evaluated: {e}  Best move value: {v}".format(
				d=depth, c=alphabeta.n_created_nodes, e=alphabeta.n_evaluated_nodes, v=value))
		print(node.cf.to_human_readable_string())

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
