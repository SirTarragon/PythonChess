# 8 x 8 grid is the normal chess game size
# 0 - 7

class Piece:
    # _x, _y, _player
    # _x, _y should be stored as numerical data
    # player should be stored as either 1 or -1

    def __init__(self, x, y, player):
        # constructor for the class
        self._x = x
        self._y = y
        self._player = player

    # Update Functions ==========================
    def updateCoordinate(self, x, y):
        self._x = x
        self._y = y

    def updatePlayer(self, player):
        self._player = player

    # Get Functions =============================
    def getCoordinate(self):
        return (self._x, self._y)

    def getPlayer(self):
        return self._player

class Pawn(Piece):
    # Movement Function =========================
    def movePiece(self, distance_y):
        # distance should usually be 1
        for x in getMoveRange():    # validate movement is in movement range
            if(x == (self._x, self._y + (self._player * distance_y)):
                self.updateCoordinate(self._x, self._y + (self._player * distance_y))
                return True # it is so return true
        return False    # distance is not acceptable so return False

    # Range Functions ===========================
    def getMoveRange(self):
        if self._player == -1 and self._y == 6:
            # bottom of screen is player 2, starting position is 6 of 7
            return {(self._x, (self._y - 1)), (self._x, (self._y - 2))}
        elif self._player == -1:
            return {(self._x, (self._y - 1))}
        elif self._player == 1 and self._y == 1:
            # top of screen is player 1, starting position for pawn is 1 of 7
            return {(self._x, (self._y + 1)), (self._x, (self._y + 2))}
        elif self._player == 1:
            return {(self._x, (self._y + 1))}

    def getCaptureRange(self):
        return {((self._x - 1),(self._y + self._player)),((self._x + 1),(self._y + self._player))}

class Rook(Piece):
    # Movement Function ==========================
    def movePiece(self, distance_x, distance_y):

    # Range Functions ===========================
    def getMoveRange(self):

    def getCaptureRange(self):
        return getMoveRange()

class Bishop(Piece):
    # Movement Function ==========================
    def movePiece(self, distance_x, distance_y):

    # Range Functions ===========================
    def getMoveRange(self):

    def getCaptureRange(self):
        return getMoveRange()

class Knight(Piece):
    # Movement Function ==========================
    def movePiece(self, distance_x, distance_y):

    # Range Functions ===========================
    def getMoveRange(self):

    def getCaptureRange(self):
        return getMoveRange()

class Queen(Piece):
    # Movement Function ==========================
    def movePiece(self, distance_x, distance_y):

    # Range Functions ===========================
    def getMoveRange(self):

    def getCaptureRange(self):
        return getMoveRange()

class King(Piece):
    # Movement Function ==========================
    def movePiece(self, distance_x, distance_y):

    # Range Functions ===========================
    def getMoveRange(self):

    def getCaptureRange(self):
        return getMoveRange()
