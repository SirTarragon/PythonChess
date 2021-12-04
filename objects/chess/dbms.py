import sqlite3
from typing import List



def createTable():
    connection = sqlite3.connect('pychess.db')
    cursor = connection.cursor()
    boardStateTableCreate = """
        CREATE TABLE IF NOT EXISTS
        BoardState(
            piece CHAR(6) NOT NULL, 
            color BOOLEAN,
            moved BOOLEAN, 
            row INTEGER, 
            column INTEGER, 
            turn BOOLEAN,
            turnNum INTEGER,
            PRIMARY KEY (row, column, turnNum)
            )
        """
    cursor.execute(boardStateTableCreate)    
    cursor.close()
    connection.close()


def loadState(turnNumber) -> List[tuple]:
    # Returns data to load the board at a previous turn number
    connection = sqlite3.connect('pychess.db')
    cursor = connection.cursor()

    query = """
		SELECT piece, color, moved, row, column, turn
		FROM BoardState
		WHERE turnNum = """ + str(turnNumber)

    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def saveState(*args) -> bool:
    # Stores board state into database
    connection = sqlite3.connect('pychess.db')
    cursor = connection.cursor()
    query = """
		INSERT INTO BoardState(piece, color, moved, row, column, turn, turnNum)
		VALUES (?,?,?,?,?,?,?)
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


def clearState() -> bool:
    print("Clearing table")
    connection = sqlite3.connect('pychess.db')
    cursor = connection.cursor()
    query = """
    DROP TABLE BoardState
    """
    try:
        cursor.execute(query)
        connection.commit()
        createTable()
    except:
        return False
    finally:
        cursor.close()
        connection.close()
        return True


def printTable() -> None:
    print("Printing table")
    connection = sqlite3.connect('pychess.db')
    cursor = connection.cursor()
    res = cursor.execute("SELECT * FROM BoardState")
    for r in res:
        print(r)
    cursor.close()
    connection.close()