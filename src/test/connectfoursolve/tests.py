import unittest

from connectfoursolve.connectfour import ConnectFour

class TestSuite(unittest.TestCase):
	def test_init(self):
		cf = ConnectFour()
		self.assertEqual(cf.get_number_of_discs(), 0)
		self.assertEqual(cf.get_current_player(), 0)
		self.assertIsNone(cf.get_winner())
		self.assertEqual(ConnectFour.width, 7)
		self.assertEqual(ConnectFour.height, 6)
	
	def test_place_disc(self):
		# .......
		# .......
		# ..?....
		# ..X....
		# ..XOOO.
		# .OXXXO.
		positions = [
			(2,0), (1,0),
			(3,0), (3,1),
			(4,0), (5,0),
			(2,1), (4,1),
			(2,2), (5,1)
		]
		cf = ConnectFour()
		for i in range(len(positions)):
			(x,y) = positions[i]
			self.assertTrue(cf.place_disc(x))
			self.assertEqual(cf.get_number_of_discs(), i+1)
			self.assertEqual(cf.discs[x][y], i % 2)
			self.assertEqual(cf.get_current_player(), (i+1) % 2)
			self.assertIsNone(cf.get_winner())
		self.assertTrue(cf.place_disc(2))
		self.assertEqual(cf.get_winner(), 0)
		
		cf = ConnectFour()
		try:
			cf.place_disc(-1)
			self.fail("Expected ValueError")
		except ValueError:
			pass
		try:
			cf.place_disc(ConnectFour.width)
			self.fail("Expected ValueError")
		except ValueError:
			pass
		for i in range(ConnectFour.height):
			self.assertTrue(cf.place_disc(4))
		self.assertFalse(cf.place_disc(4))
	
	def test_get_heuristic_value_win(self):
		# Horizontal win for player 0 (X)
		string_list = [
			".......",
			".......",
			".......",
			".......",
			"..OO...",
			".OXXXX.",
		]
		self.asserts_for_heuristic_value(string_list, 7, 1, 1000042-7)
		# Vertical win for player 1 (O)
		string_list = [
			".......",
			".......",
			"O......",
			"O......",
			"O..XX..",
			"O..XX..",
		]
		self.asserts_for_heuristic_value(string_list, 8, 0, -1000042+8)
		# Diagonal (/) top-left
		string_list = [
			"...O...",
			"..OX...",
			".OXO...",
			"OXOX...",
			"OXXO...",
			"XXOX...",
		]
		self.asserts_for_heuristic_value(string_list, 18, 0, -1000042+18)
		# Diagonal (\) top-right
		string_list = [
			"...O...",
			"...XO..",
			"...OXO.",
			"...XOXO",
			"...OXXO",
			"...XOXX",
		]
		self.asserts_for_heuristic_value(string_list, 18, 0, -1000042+18)
		# Diagonal (\) top-left
		string_list = [
			"X......",
			"XX.....",
			"OXX....",
			"XOOX...",
			"OXXO...",
			"OOOXO..",
		]
		self.asserts_for_heuristic_value(string_list, 19, 1, 1000042-19)
		# Diagonal (/) top-right
		string_list = [
			"......X",
			".....XX",
			"....XXO",
			"...XOOX",
			"...OXXO",
			"..OXOOO",
		]
		self.asserts_for_heuristic_value(string_list, 19, 1, 1000042-19)
		# Diagonal (\) bottom-left
		string_list = [
			".......",
			".......",
			"O......",
			"XO.....",
			"OXO....",
			"XXXO...",
		]
		self.asserts_for_heuristic_value(string_list, 10, 0, -1000042+10)
		# Diagonal (/) bottom-right
		string_list = [
			".......",
			".......",
			"......O",
			".....OX",
			"....OXO",
			"...OXXX",
		]
		self.asserts_for_heuristic_value(string_list, 10, 0, -1000042+10)
		# Diagonal (/) bottom-left
		string_list = [
			".......",
			".......",
			"...X...",
			"..XX...",
			".XOO...",
			"XOXOO..",
		]
		self.asserts_for_heuristic_value(string_list, 11, 1, 1000042-11)
		# Diagonal (\) bottom-right
		string_list = [
			".......",
			".......",
			"...X...",
			"...XX..",
			"...OOX.",
			"..OOXOX",
		]
		self.asserts_for_heuristic_value(string_list, 11, 1, 1000042-11)
	
	def test_get_heuristic_value_almost_win(self):
		string_list = [
			".......",
			".......",
			".......",
			".......",
			"..OOO..",
			"..XXX..",
		]
		self.asserts_for_heuristic_value(string_list, 6, 0, 1000042-7)
		string_list = [
			".......",
			".......",
			".......",
			".......",
			"XX.....",
			"XX..OOO",
		]
		self.asserts_for_heuristic_value(string_list, 7, 1, -1000042+8)
		string_list = [
			".......",
			".......",
			".......",
			".......",
			"..OO...",
			".XXX...",
		]
		self.asserts_for_heuristic_value(string_list, 5, 1, 1000042-7)
		string_list = [
			".......",
			".......",
			".......",
			".......",
			"X......",
			"XX.OOO.",
		]
		self.asserts_for_heuristic_value(string_list, 6, 0, -1000042+8)
		string_list = [
			".......",
			".......",
			"..X..X.",
			"..O?XO.",
			"..O?XO.",
			".XXOOX.",
		]
		self.asserts_for_heuristic_value(string_list, 13, 1, 1000042-15)
	
	def test_get_heuristic_value_immediate_threat_no_choice(self):
		string_list = [
			".......",
			"..X....",
			"..O....",
			"..XXO..",
			"..OOXO.",
			"..OXXXO",
		]
		self.asserts_for_heuristic_value(string_list, 14, 0, -1)
		# "X" to move. "O" has an immediate threat in column 2.
		# "X" must place in column 2, multiple immediate threats (columns 2 and 4).
		# "X" wins after 2 additional moves.
		string_list = [
			".......",
			".......",
			"...X...",
			".X.XX..",
			"XO.OO..",
			"OXOXOO.",
		]
		self.asserts_for_heuristic_value(string_list, 14, 0, 1000042-17)

	def asserts_for_heuristic_value(self, cf_as_string_list, number_of_discs, current_player,
	                                heuristic_value):
		cf = string_list_to_connect_four(cf_as_string_list)
		self.assertEqual(cf.get_number_of_discs(), number_of_discs)
		self.assertEqual(cf.get_current_player(), current_player)
		#print("Get heuristic value for:")
		#print(cf.to_human_readable_string())
		self.assertEqual(cf.get_heuristic_value(), heuristic_value)

def string_list_to_connect_four(string_list):
	symbol_to_player = {"X": 0, "O": 1}
	cf = ConnectFour()
	for y in range(ConnectFour.height):
		line = string_list[ConnectFour.height-1-y]
		for x in range(ConnectFour.width):
			symbol = line[x]
			try:
				cf.discs[x][y] = symbol_to_player[symbol]
			except KeyError:
				pass
	return cf

if __name__ == "__main__":
	unittest.main()
