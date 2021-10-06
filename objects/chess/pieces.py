# 8 x 8 grid is the normal chess game size
# 0 - 7
# these values should be able to be changed through the module
_board-game_x = 8
_board-game_y = 8

def updateGameSize(x, y):
  _board-game_x = x
  _board-game_y = y

class Piece:
    # _x, _y, _player
    # _x, _y should be stored as numerical data
    # player should be stored as either 1 or -1
    # this is because the grid goes from
    #   0 1 2 3 4 5 6 7
    # 0 R K B C Q B K R
    # 1 P P P P P P P P
    # 2 . . . . . . . .
    # 3 . . . . . . . .
    # 4 . . . . . . . .
    # 5 . . . . . . . .
    # 6 P P P P P P P P
    # 7 R K B C Q B K R

    # With one player starting near the top with units moving down,
    # and the other starting from the bottom with units moving up.
    # However that's from the perspective of the player, bottom moving
    # up would be subtracting from the grid value to go "up"

    def __init__(self, x: int, y: int, player: int) -> None:
        # constructor for the class
        # we're under the assumption that the input values for the player/team are correct
        self._x = x
        self._y = y
        self._player = player

    # Update Functions ==========================
    def updateCoordinate(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def updatePlayer(self, player: int) -> None:
        self._player = player

    # Get Functions =============================
    def getCoordinate(self) -> tuple:
        return (self._x, self._y)

    def getXValue(self) -> int:  # for checking to make sure
        return self._x
    
    def getYValue(self) -> int:
        return self._y

    def getPlayer(self) -> int:
        return self._player

class Pawn(Piece):
    # Movement Function =========================
    def movePiece(self, distance_y: int):
        # distance should usually be 1
        for i in self.getMoveRange():    # validate movement is in movement range
            if(i == (self._x, self._y + (self._player * distance_y)):
                self.updateCoordinate(self._x, self._y + (self._player * distance_y))
                return True # it is so return true
        return False    # distance is not acceptable so return False

    # Range Functions ===========================
    def getMoveRange(self):
        if self._player == -1 and self._y == 6:
            # bottom of screen is player 2, starting position is 6 of 7
            return {(self._x, (self._y - 1)), (self._x, (self._y - 2))}
        elif self._player == 1 and self._y == 1:
            # top of screen is player 1, starting position for pawn is 1 of 7
            return {(self._x, (self._y + 1)), (self._x, (self._y + 2))}
        else:
            if(0 <= (self._y + self._player) and (self._y + self._player) < _board-game_y):
              return {(self._x, (self._y + self._player))}
            else:
              return {(self._x, self._y)}

    def getCaptureRange(self):
        return {((self._x - 1),(self._y + self._player)),((self._x + 1),(self._y + self._player))}

class Rook(Piece):
    # let's say grid is like:
    # 0 1 2 3 4 5 6 7
    # . . . . . . . .
    # . . . . . . . .
    # . . . . R . . .
    # . . . . . . . .
    # . . . . . . . .

    # Possible moves of the ROOK is:
    # 0 1 2 3 4 5 6 7
    # . . . . * . . .
    # . . . . * . . .
    # * * * * R * * *
    # . . . . * . . .
    # . . . . * . . .

    # Movement Function ==========================
    def movePiece(self, distance_x: int, distance_y: int):
      for i in self.getMoveRange():
        if(i == (self._x + (self._player * distance_x), self._y + (self._player * distance_y)):
          self.updateCoordinate((self._x + (self._player * distance_x), self._y + (self._player * distance_y))
          return True # movement distance is within movement rnage, return true
      return False  # it is not so return false

    # Range Functions ===========================
    def getMoveRange(self):
      # move range of ROOK is vertical and horizontal of piece
      # so depending on player number
      moveRange = {}
      for i in range(_board-game_x):
        if(i != self._x)
          moveRange.add((i,self._y))
      for i in range(_board-game_y):
        if(i != self._y):
          moveRange.add((self._x, i))

      return moveRange

    def getCaptureRange(self):
        return self.getMoveRange()

class Bishop(Piece):
    # let's say grid is like:
    # 0 1 2 3 4 5 6 7
    # . . . . . . . .
    # . . . . . . . .
    # . . . . B . . .
    # . . . . . . . .
    # . . . . . . . .

    # Possible moves of the BISHOP is:
    # 0 1 2 3 4 5 6 7
    # . . * . . . * .
    # . . . * . * . .
    # . . . . B . . .
    # . . . * . * . .
    # . . * . . . * .

    # Movement Function ==========================
    def movePiece(self, distance_x: int, distance_y: int):
      for i in self.getMoveRange():
        if(i == (self._x + (self._player * distance_x), self._y + (self._player * distance_y)):
          self.updateCoordinate((self._x + (self._player * distance_x), self._y + (self._player * distance_y))
          return True # movement distance is within movement rnage, return true
      return False  # it is not so return false

    # Range Functions ===========================
    def getMoveRange(self):

    def getCaptureRange(self):
        return self.getMoveRange()

class Knight(Piece):
    # let's say grid is like:
    # 0 1 2 3 4 5 6 7
    # . . . . . . . .
    # . . . . . . . .
    # . . . . K . . .
    # . . . . . . . .
    # . . . . . . . .

    # Possible moves of the KNIGHT is:
    # 0 1 2 3 4 5 6 7
    # . . . * . * . .
    # . . * . . . * .
    # . . . . K . . .
    # . . * . . . * .
    # . . . * . * . .

    # so [(x-1,y-2),(x+1,y-2),(x-2,y-1),(x+2,y-1),(x-2,y+1),(x+2,y+1),(x-1,y+2),(x+1,y+2)]

    # Movement Function ==========================
    def movePiece(self, distance_x: int, distance_y: int):
      for i in self.getMoveRange():
        if(i == (self._x + (self._player * distance_x), self._y + (self._player * distance_y)):
          self.updateCoordinate((self._x + (self._player * distance_x), self._y + (self._player * distance_y))
          return True # movement distance is within movement rnage, return true
      return False  # it is not so return false

    # Range Functions ===========================
    def getMoveRange(self):
        moveRange = {(self._x-1,self._y-2),(self._x+1,self._y-2),(self._x-2,self._y-1),(self._x+2,self._y-1),(self._x-2,self._y+1),(self._x+2,self._y+1),(self._x-1,self._y+2),(self._x+1,self._y+2)} # these are the only acceptable points so far

        unacceptablePoints = {} # this holds the values of what turns out to be unacceptable

        for i in moveRange: # this goes through to find which points are outside of board range
          if (0 <= i[0] and i[0] < _board-game_x) and (0 <= i[1] and i[1] < _board-game_y):
            unacceptablePoints.add(i)

        if(len(unacceptablePoints) > 0):  # if any were, time to go through to delete them
          for i in unacceptablePoints:
            moveRange.remove(i)

        return moveRange

    def getCaptureRange(self):
        return self.getMoveRange()

class Queen(Piece):
    # let's say grid is like:
    # 0 1 2 3 4 5 6 7
    # . . . . . . . .
    # . . . . . . . .
    # . . . . Q . . .
    # . . . . . . . .
    # . . . . . . . .

    # Possible moves of the QUEEN is:
    # 0 1 2 3 4 5 6 7
    # . . * . * . * .
    # . . . * * * . .
    # * * * * Q * * *
    # . . . * * * . .
    # . . * . * . * .

    # Movement Function ==========================
    def movePiece(self, distance_x: int, distance_y: int):
      for i in self.getMoveRange():
        if(i == (self._x + (self._player * distance_x), self._y + (self._player * distance_y)):
          self.updateCoordinate((self._x + (self._player * distance_x), self._y + (self._player * distance_y))
          return True # movement distance is within movement rnage, return true
      return False  # it is not so return false

    # Range Functions ===========================
    def getMoveRange(self):

    def getCaptureRange(self):
        return self.getMoveRange()

class King(Piece):
    # let's say grid is like:
    # 0 1 2 3 4 5 6 7
    # . . . . . . . .
    # . . . . . . . .
    # . . . . C . . .
    # . . . . . . . .
    # . . . . . . . .

    # Possible moves of the KING is:
    # 0 1 2 3 4 5 6 7
    # . . . . . . . .
    # . . . * * * . .
    # . . . * C * . .
    # . . . * * * . .
    # . . . . . . . .

    # Movement Function ==========================
    def movePiece(self, distance_x: int, distance_y: int):
      for i in self.getMoveRange():
        if(i == (self._x + (self._player * distance_x), self._y + (self._player * distance_y)):
          self.updateCoordinate((self._x + (self._player * distance_x), self._y + (self._player * distance_y))
          return True # movement distance is within movement rnage, return true
      return False  # it is not so return false

    # Range Functions ===========================
    def getMoveRange(self):

    def getCaptureRange(self):
        return self.getMoveRange()