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

def set_value_of_state(db, state, value, move):
	cursor = db.cursor()
	sql = "insert into connectfour (state, value, move) values (%s, %s, %s)"
	cursor.execute(sql, (state, value, move))
	db.commit()

def get_number_of_rows(db):
	cursor = db.cursor()
	sql = "select * from connectfour"
	cursor.execute(sql)
	return len(cursor.fetchall())
