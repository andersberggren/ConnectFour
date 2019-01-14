import unittest

from connectfoursolve.connectfour import ConnectFour

class Test(unittest.TestCase):
	def test_init(self):
		cf = ConnectFour()
		self.assertEqual(cf.get_number_of_discs(), 0)
		self.assertEqual(cf.get_current_player(), 0)
		self.assertIsNone(cf.get_winner())
		self.assertEqual(ConnectFour.width, 7)
		self.assertEqual(ConnectFour.height, 6)
	
	def test_place_disc(self):
		cf = ConnectFour()
		for i in range(ConnectFour.height):  # @UnusedVariable
			self.assertTrue(cf.place_disc(4))
		self.assertTrue(cf.place_disc(3))
		self.assertFalse(cf.place_disc(4))
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
	
	def test_play_game(self):
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
