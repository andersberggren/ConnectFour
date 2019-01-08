from connectfoursolve.connectfour import ConnectFour
from connectfoursolve.db import connect_to_db, get_value_of_state, set_value_of_state, get_number_of_rows
from connectfoursolve.searchnode import SearchNode

def print_cf(cf):
	s = cf.get_state_as_string()
	while len(s) > 0:
		row = s[-ConnectFour.width:]
		s = s[:-ConnectFour.width]
		print(row)
	print("Winner:", cf.get_winner())

if __name__ == "__main__":
	db_connection = connect_to_db()
	#db_connection.cursor().execute("delete from connectfour")
	#db_connection.commit()
	print("Number of rows: ", get_number_of_rows(db_connection))
	nodes = [SearchNode(ConnectFour())]
	evaluated_nodes = set()
	n_nodes = len(nodes)
	n_winners = 0
	while n_winners < 10000 and len(nodes) > 0 and n_winners < 400:
		node = nodes.pop(0)
		node_state = node.cf.get_state_as_string()
		#for successor in sorted(node.get_successors(), key=lambda x: 0, reverse=True):
		for successor in node.get_successors():
			n_nodes += 1
			successor_state = successor.cf.get_state_as_string()
			if successor_state in evaluated_nodes:
				continue
			evaluated_nodes.add(successor_state)
			winner = successor.cf.get_winner()
			successor_value = get_value_of_state(db_connection, successor_state)
			if successor_value is not None:
				n_winners += 1
				set_value_of_state(db_connection, node.cf.get_state_as_string(), successor_value, successor.cf.move)
				continue
			if winner is not None:
				n_winners += 1
				print("New winner!")
				print_cf(successor.cf)
				set_value_of_state(db_connection, successor_state, [1000000, -1000000][winner], -1)
			else:
				#nodes.insert(0, successor)
				nodes.append(successor)
	print("New winners:", n_winners)
