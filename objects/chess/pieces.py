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
    # _x, _y should be stored as int, 0-7
    # player should be stored as either 1 or -1

    # player is this way instead of a boolean for calculation purposes
    # this is because the grid goes in a normal chess game:

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
        # we're under the assumption that the input values are correct
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

# P A W N ===========================================================================
class Pawn(Piece):
    # let's say grid is like:
    # 0 1 2 3 4 5 6 7
    # . . . . . . . .
    # . . . . . . . .
    # . . . . P . . .
    # . . . . . . . .
    # . . . . . . . .

    # Possible moves of the PAWN is:
    # 0 1 2 3 4 5 6 7
    # . . . . . . . .
    # . . . . . . . .
    # . . . . P . . .
    # . . . . * . . .
    # . . . . . . . .

    # while for capturing:
    # 0 1 2 3 4 5 6 7
    # . . . . . . . .
    # . . . . . . . .
    # . . . . P . . .
    # . . . * . * . .
    # . . . . . . . .

    # Movement Function =========================
    def movePiece(self, distance_y: int):
        # distance should usually be 1
        for i in self._moveRange:    # validate movement is in movement range
            if(i == (self._x, self._y + (self._player * distance_y)):
                self.updateCoordinate(self._x, self._y + (self._player * distance_y))
                return True # it is so return true
        return False    # distance is not acceptable so return False

    # Calculate Functions =======================
    def calcMoveRange(self):
        if self._player == -1 and self._y == 6:
            # bottom of screen is player 2, starting position is 6 of 7
            self._moveRange = {(self._x, (self._y - 1)), (self._x, (self._y - 2))}
        elif self._player == 1 and self._y == 1:
            # top of screen is player 1, starting position for pawn is 1 of 7
            self._moveRange = {(self._x, (self._y + 1)), (self._x, (self._y + 2))}
        else:
            if(0 <= (self._y + self._player) and (self._y + self._player) < _board-game_y):
              self._moveRange = {(self._x, (self._y + self._player))}
            else:
              self._moveRange = {(self._x, self._y)}

    def calcCaptureRange(self):
        self._captRange = {((self._x - 1),(self._y + self._player)),((self._x + 1),(self._y + self._player))}

    # Range Functions ===========================
    def getMoveRange(self):
        return self._moveRange

    def getCaptureRange(self):
        return self._captRange

# R O O K ===========================================================================
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
      for i in self._moveRange:
        if(i == (self._x + (self._player * distance_x), self._y + (self._player * distance_y)):
          self.updateCoordinate((self._x + (self._player * distance_x), self._y + (self._player * distance_y))
          return True # movement distance is within movement range, return true
      return False  # it is not so return false

    # Calculate Functions =======================
    def calcMoveRange(self):
      # move range of ROOK is vertical and horizontal of piece
      # so depending on player number
      self._moveRange = {}

      # handles the X axis for the ROOK
      for i in range(_board-game_x):
        if(i != self._x)
          self._moveRange.add((i,self._y))

      # handles the Y axis for the ROOK
      for i in range(_board-game_y):
        if(i != self._y):
          self._moveRange.add((self._x, i))

    def calcCaptureRange(self):
        self._captRange = self._moveRange

    # Range Functions ===========================
    def getMoveRange(self):
        return self._moveRange

    def getCaptureRange(self):
        return self._captRange

# B I S H O P =======================================================================
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
      for i in self._moveRange:
        if(i == (self._x + (self._player * distance_x), self._y + (self._player * distance_y)):
          self.updateCoordinate((self._x + (self._player * distance_x), self._y + (self._player * distance_y))
          return True # movement distance is within movement range, return true
      return False  # it is not so return false

    # Calculate Functions =======================
    def calcMoveRange(self):
      self._moveRange = {}

      # handles above the BISHOP point. So from 0 to BISHOP actual Y
      for i in range(self._y + 1):
        if(i != 0):
          self._moveRange.add((self._x - i, self._y - i))
          self._moveRange.add((self._x + i, self._y - i))
      
      # handles the rest from the BISHOP point. So from BISHOP Y to the board game edge
      for i in range(self._y, _board-game_y):
        if(i != 0):
          self._moveRange.add((self._x - i, self._y + i))
          self._moveRange.add((self._x + i, self._y + i))

    def calcCaptureRange(self):
        self._captRange = self._moveRange

    # Range Functions ===========================
    def getMoveRange(self):
        return self._moveRange

    def getCaptureRange(self):
        return self._captRange

# K N I G H T =======================================================================
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
      for i in self._moveRange:
        if(i == (self._x + (self._player * distance_x), self._y + (self._player * distance_y)):
          self.updateCoordinate((self._x + (self._player * distance_x), self._y + (self._player * distance_y))
          return True # movement distance is within movement range, return true
      return False  # it is not so return false

    # Calculate Functions =======================
    def calcMoveRange(self):
        self._moveRange = {(self._x-1,self._y-2),(self._x+1,self._y-2),(self._x-2,self._y-1),(self._x+2,self._y-1),(self._x-2,self._y+1),(self._x+2,self._y+1),(self._x-1,self._y+2),(self._x+1,self._y+2)} # these are the only acceptable points so far

        unacceptablePoints = {} # this holds the values of what turns out to be unacceptable

        for i in self._moveRange: # this goes through to find which points are outside of board range
          if (0 <= i[0] and i[0] < _board-game_x) and (0 <= i[1] and i[1] < _board-game_y):
            unacceptablePoints.add(i)

        if(len(unacceptablePoints) > 0):  # if any were, time to go through to delete them
          for i in unacceptablePoints:
            self._moveRange.remove(i)

    def calcCaptureRange(self):
        self._captRange = self._moveRange

    # Range Functions ===========================
    def getMoveRange(self):
        return self._moveRange

    def getCaptureRange(self):
        return self._captRange

# Q U E E N =========================================================================
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
      for i in self._moveRange:
        if(i == (self._x + (self._player * distance_x), self._y + (self._player * distance_y)):
          self.updateCoordinate((self._x + (self._player * distance_x), self._y + (self._player * distance_y))
          return True # movement distance is within movement range, return true
      return False  # it is not so return false

    # Calculate Functions =======================
    def calcMoveRange(self):
      self._moveRange = {}

      # handles the X axis for the ROOK
      for i in range(_board-game_x):
        if(i != self._x)
          self._moveRange.add((i,self._y))

      # handles the Y axis for the ROOK
      for i in range(_board-game_y):
        if(i != self._y):
          self._moveRange.add((self._x, i))

      # handles above the BISHOP point. So from 0 to BISHOP actual Y
      for i in range(self._y + 1):
        if(i != 0):
          self._moveRange.add((self._x - i, self._y - i))
          self._moveRange.add((self._x + i, self._y - i))
      
      # handles the rest from the BISHOP point. So from BISHOP Y to the board game edge
      for i in range(self._y, _board-game_y):
        if(i != 0):
          self._moveRange.add((self._x - i, self._y + i))
          self._moveRange.add((self._x + i, self._y + i))

    def calcCaptureRange(self):
        self._captRange = self._moveRange

    # Range Functions ===========================
    def getMoveRange(self):
        return self._moveRange

    def getCaptureRange(self):
        return self._captRange

# K I N G ===========================================================================
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
          return True # movement distance is within movement range, return true
      return False  # it is not so return false

    # Calculate Functions =======================
    def calcMoveRange(self):
      self._moveRange = {}


    def calcCaptureRange(self):
        self._captRange = self._moveRange

    # Range Functions ===========================
    def getMoveRange(self):
        return self._moveRange

    def getCaptureRange(self):
        return self._captRange