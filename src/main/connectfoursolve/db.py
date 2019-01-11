import mysql.connector

def connect_to_db(*, host="localhost", database="pytestdb", user="pyuser", passwd="pypassword"):
	try:
		db_connection = mysql.connector.connect(
			host=host,
			database=database,
			user=user,
			passwd=passwd
		)
	except mysql.connector.Error as err:
		print("Error raised when connecting to database:", err)
		raise err
	return db_connection

def get_value_of_state(db, state):
	cursor = db.cursor()
	sql = "select value from connectfour where state = %s"
	cursor.execute(sql, (state,))
	row = cursor.fetchone()
	return row[0] if row is not None else None

def set_value_of_state(db, state, value):
	cursor = db.cursor()
	sql = "replace into connectfour (state, value) values (%s, %s)"
	cursor.execute(sql, (state, value))
	db.commit()

def get_number_of_rows(db):
	cursor = db.cursor()
	sql = "select count(*) from connectfour"
	cursor.execute(sql)
	return int(cursor.fetchone()[0])

def add_fringe(db, states, depth):
	cursor = db.cursor()
	sql = "replace into fringe (state, depth) values (%s, %s)"
	cursor.executemany(sql, [(state, depth) for state in states])
	db.commit()

def get_fringe(db):
	cursor = db.cursor()
	sql = "select state, depth from fringe where depth in (select max(depth) from fringe)"
	cursor.execute(sql)
	return cursor
