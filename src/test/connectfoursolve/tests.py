import unittest

from connectfoursolve.connectfour import ConnectFour

class TestSuite(unittest.TestCase):
	def test_init(self):
		cf = ConnectFour()
		self.assertEqual(len(cf.position_to_disc), 0)
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
			position = positions[i]
			column = position[0]
			cf.place_disc(column)
			self.assertEqual(len(cf.position_to_disc), i+1)
			self.assertEqual(cf.position_to_disc[position], i % 2)
			self.assertEqual(cf.get_current_player(), (i+1) % 2)
			self.assertIsNone(cf.get_winner())
		cf.place_disc(2)
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
			cf.place_disc(4)
		try:
			cf.place_disc(4)
			self.fail("Expected ValueError")
		except ValueError:
			pass
	
	def test_get_heuristic_value(self):
		string_list = [
			".......",
			".......",
			".......",
			".......",
			"..OO...",
			".OXXXX.",
		]
		self.asserts_for_heuristic_value(string_list, 7, 1, 1000042-7)
		string_list = [
			".......",
			".......",
			"O......",
			"O......",
			"O..XX..",
			"O..XX..",
		]
		self.asserts_for_heuristic_value(string_list, 8, 0, -1000042+8)
	
	def asserts_for_heuristic_value(self, cf_as_string_list, number_of_discs, current_player,
	                                heuristic_value):
		cf = string_list_to_connect_four(cf_as_string_list)
		self.assertEqual(len(cf.position_to_disc), number_of_discs)
		self.assertEqual(cf.get_current_player(), current_player)
		self.assertEqual(cf.get_heuristic_value(), heuristic_value)

def string_list_to_connect_four(string_list):
	symbol_to_player = {"X": 0, "O": 1}
	cf = ConnectFour()
	for y in range(ConnectFour.height):
		line = string_list[ConnectFour.height-1-y]
		for x in range(ConnectFour.width):
			symbol = line[x]
			try:
				cf.position_to_disc[(x,y)] = symbol_to_player[symbol]
			except KeyError:
				pass
	return cf

if __name__ == "__main__":
	unittest.main()
