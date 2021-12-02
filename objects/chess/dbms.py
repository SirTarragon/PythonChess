import sqlite3
from typing import List

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
		turnNum INTEGER
		)
	"""
cursor.execute(boardStateTableCreate)

cursor.close()
connection.close()

#Returns data to load the board at a previous turn number
def loadState(turnNumber) -> List[tuple]:
	connection = sqlite3.connect('pychess.db')
	cursor = connection.cursor()

	query = """
		SELECT piece, color, row, column
		FROM BoardState
		WHERE turnNum = """ + str(turnNumber)

	cursor.execute(query)

	result = cursor.fetchall()

	cursor.close()
	connection.close()

	return result

#Stores board state into database
def saveState(*args) -> bool:
	connection = sqlite3.connect('pychess.db')
	cursor = connection.cursor()
	query = """
		INSERT INTO BoardState(piece, color, row, column, turn, turnNum)
		VALUES (?,?,?,?,?,?)
		"""

	try:
		cursor.execute(query, args)
		connection.commit()
	except:
		return False
	finally:
		cursor.close()
		connection.close()
		return True		
