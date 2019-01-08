from connectfoursolve.connectfour import ConnectFour
from connectfoursolve.db import connect_to_db, get_value_of_state, set_value_of_state

if __name__ == "__main__":
	db_connection = connect_to_db()
	#set_value_of_state(db_connection, "asdf", 7)
	#value = get_value_of_state(db_connection, "asdf")
	#print(value)
	cf = ConnectFour()
	#for i in [2, 4, 4, 1, 4, 0, 4, 6, 4]:
	for i in [0, 3,4, 4,5, 6,5, 5,6, 0,6, 6]:
		cf.place_disc(i)
		s = cf.get_state_as_string()
		while len(s) > 0:
			row = s[-ConnectFour.width:]
			s = s[:-ConnectFour.width]
			print(row)
		print("Winner:", cf.get_winner())
