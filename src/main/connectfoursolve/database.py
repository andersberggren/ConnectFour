import mysql.connector

class DatabaseConnection:
	def __init__(self):
		self.db = None
		self.connect()
	
	def connect(self):
		try:
			self.db = mysql.connector.connect(
				host="localhost",
				database="pytestdb",
				user="pyuser",
				passwd="pypassword"
			)
		except mysql.connector.Error as err:
			print("Error raised when connecting to database:", err)
			raise err
	
	def execute_sql(self, sql):
		cursor = self.db.cursor()
		cursor.execute(sql)
		return cursor
		
	def execute_sql_and_commit(self, sql):
		cursor = self.db.cursor()
		cursor.execute(sql)
		self.db.commit()
	
	def get_number_of_solved_states(self):
		cursor = self.db.cursor()
		sql = "select count(*) from connectfour"
		cursor.execute(sql)
		return int(cursor.fetchone()[0])
	
	def get_value_of_state(self, state):
		cursor = self.db.cursor()
		sql = "select value from connectfour where state = %s"
		cursor.execute(sql, (state,))
		row = cursor.fetchone()
		return row[0] if row is not None else None
	
	def set_value_of_state(self, state, value):
		cursor = self.db.cursor()
		sql = "replace into connectfour (state, value) values (%s, %s)"
		cursor.execute(sql, (state, value))
		self.db.commit()
	
	def get_fringe(self):
		"""
		Returns a cursor to all rows in table "fringe" with max depth.
		"""
		cursor = self.db.cursor()
		sql = "select state, depth from fringe where depth in (select max(depth) from fringe)"
		cursor.execute(sql)
		return cursor
	
	def add_fringe(self, states, depth):
		cursor = self.db.cursor()
		sql = "replace into fringe (state, depth) values (%s, %s)"
		cursor.executemany(sql, [(state, depth) for state in states])
		self.db.commit()
