import sqlite3

#Create connection and cursor

connection = sqlite3.connect('pychess.db')
cursor = connection.cursor()

#Create all tables if they don't already exist

boardStateTableCreate = """
	CREATE TABLE IF NOT EXISTS
	BoardState(
		piece CHAR(6) NOT NULL, 
		color BOOLEAN, 
		row INTEGER, 
		column INTEGER, 
		turn BOOLEAN,
		turnNum INTEGER,
		PRIMARY KEY (piece, color, turnNum)
		)
	"""
cursor.execute(boardStateTableCreate)

cursor.close()
connection.close()

#Returns data to load the board at a previous turn number
def loadState(turnNumber) -> list(tuple()):
	connection = sqlite3.connect('pychess.db')
	cursor = connection.cursor()

	query = """
		SELECT piece, color, row, column
		FROM BoardState
		WHERE turnNum = turnNumber
	"""
	cursor.execute(query)

	result = cursor.fetchall()

	cursor.close()
	connection.close()

	return result

#Stores board state into database
def saveState(pc, c, r, col, t, tn) -> bool:
	connection = sqlite3.connect('pychess.db')
	cursor = connection.cursor()

	query = """
		INSERT INTO BoardState(piece, color, row, col, turn, turnNum)
		VALUES (?,?,?,?,?,?)
		"""
	args = (pc, c, r, col, t, tn)

	try:
		cursor.execute(query, args)
		connection.commit()
	except:
		return False
	finally:
		cursor.close()
		connection.close()
		return True		
