import copy
import math
from typing import List, cast

try:
  import pieces as pieces
except ModuleNotFoundError:
  from . import pieces as pieces
try:
  import dbms as db
except ModuleNotFoundError:
  from . import dbms as db
try:
  from enums import PieceType as Type, GameState as State
except ModuleNotFoundError:
  from .enums import PieceType as Type, GameState as State
from itertools import permutations

# A Chess instance is a game of chess
# Game logic for new game:
# Create an instance of Chess
# user calls valid_move on a square
# valid move iterates over squares
# using can_move to check if the piece can_move there


class Chess:
    def __init__(self) -> None:
        """
        Chess() -> initializes default chess game
        """
        self._board = Chess.get_starting_board()
        self._turn = True  # True indicates whether or not it's white's turn
        self._game_state = State.NORMAL
        self._turnNum = 0
        self._enpassant = None
        self._castle = False
        #self.save_board()


    def __str__(self) -> str:
        board = " 01234567\n"
        for x in range(8):
            board += str(x)
            for y in range(8):
                board += str("." if not self._board[x][y] else self._board[x][y])
            board += "\n"
        return board


    def attempt_move(self, to_move: tuple, move_to: tuple) -> State:
        """(to_move: tuple, move_to: tuple) -> State
        Takes 2 tuples of 2 ints each, [0-7], where the first tuple represents
        the location of a piece to move, and the 2nd tuple represents the
        location to move to.

        returns type State, an enum representing the resulting gamestate
        after the move is processed. In the event that invalid input is passed
        the gamestate will not change, then it's incumbent upon a user to check the
        turn has (hasn't) changed.
        """
        row1, col1 = to_move
        row2, col2 = move_to
        # validate data passed:
        # Check that locations passed are vald
        if Chess.__out_of_bounds((row1, col1, row2, col2)):
            return self._game_state
        piece_to_move = self._board[row1][col1]
        # Check for a piece to move at to_move
        if not piece_to_move:
            return self._game_state
        if piece_to_move.is_white() != self._turn:
            return self._game_state
        # Check for actual move attempt
        if to_move == move_to:
            return self._game_state

        # Check if the piece selected can move to the desired location
        # can_move will handle the brunt of the game logic
        if not self.__can_move(to_move, move_to):
            return self._game_state

        return self.__move_piece(to_move, move_to)


    def valid_moves(self, to_move: tuple) -> tuple:
        """(to_move: tuple) -> tuple
        returns the tuple of tuples where each element is
        a (row, col) ([0-7],[0-7]), to which a piece may move
        If the move is 'possible' but results in check/checkmate, it will not
        be included.
        """
        # Returns a tuple of tuples
        # Each tuple is a row,col to which the piece located @to_move may move to
        # returns empty tuple if no valid moves available, or invalid input
        # Easiest way I think would be validating to_move and then calling can_move on all squares
        # index and return any that return true, although that may prove inefficient
        moves = []
        for i in range(8):
            for x in range(8):
                if self.__can_move(to_move, (i,x)):
                    moves.append((i,x))
        return moves


    def resign(self, playerColor: bool = False):
        """(playerColor: bool)-> State.NAME
        resigns the player of the current turn
        """
        self._game_state = State.WHITE_CHECKMATED if playerColor else State.BLACK_CHECKMATED
        self._turnNum += 1
        print("Player resigned, results of match: " + str(self._game_state))
        return self._game_state.name


    def promote(self, move_to: tuple, piece: str = "QUEEN"):
        """(move_to: tuple, piece: str) -> State.NAME
        upgrades a pawn to another unit. Queening is default.
        """
        x,y = move_to
        print(move_to, piece)

        if piece == "ROOK":
            self._board[x][y] = pieces.Rook(not self._turn)
        if piece == "KNIGHT":
            self._board[x][y] = pieces.Knight(not self._turn)
        if piece == "BISHOP":
            self._board[x][y] = pieces.Bishop(not self._turn)
        if piece == "QUEEN":
            self._board[x][y] = pieces.Queen(not self._turn)
        self._game_state = State.NORMAL
        return self._game_state.name


    def get_board(self) -> List[List[pieces.Piece]]:
        """()-> List[List[pieces.Piece]]
        returns a deepcopy of the present board
        """
        # return copy of list to prevent modification
        # if anyone knows a less costly way of returning a copy
        # of the list, then please implement it, not that this
        # will really affect us here, I'd just be curious to know in general
        return copy.deepcopy(self._board)


    def get_turn(self) -> bool:
        """() -> bool
        returns True if white's turn, False if black
        """
        return self._turn


    def get_turnNum(self) -> int:
        """() -> int
        returns integer number of turnNum
        """
        return self._turnNum


    def __can_move(self, to_move: tuple, move_to: tuple) -> bool:
        # Assumes that to_move and move_to are in bounds
        # For bug prevention, any variations to the given bounds
        # Will get validated before accessing
        row1, col1 = to_move
        row2, col2 = move_to
        piece_to_move = self._board[row1][col1]

        # Cannot land on own piece ever, right?
        piece_to_remove = self._board[row2][col2]
        if piece_to_remove and piece_to_remove.is_white() == piece_to_move.is_white():
            return False

        # Cannot move to own spot
        if to_move == move_to:
            return False

        # Get the piece at to_move, then branch to if statements based on piece
        if piece_to_move.get_type() == Type.PAWN:
            # a pawn may move 2 spaces if not yet moved
            # one space forward anytime
            # diag to take an occupied opp
            # diag to take an empty spot if adjacent is opp pawn (en passant)
            direction = row1 - 2 if piece_to_move.is_white() else row1 + 2
            if not piece_to_move.get_moved() and not Chess.__out_of_bounds((direction,)):
                if row2 == direction and col2 == col1 and not self._board[row2][col2]:
                    # attempt to move an unmoved pawn 2 spaces to an empty space
                    # modify board
                    for i in range(row2 > row1 and row2 or row1-1, row1 if row2 > row1 else row2-1, -1):
                        if self._board[i][col1]:
                            return False
                    return self.__check_for_check(to_move, move_to)
            direction = row1 - 1 if piece_to_move.is_white() else row1 + 1
            if not Chess.__out_of_bounds((direction,)) and not self._board[row2][col2]:
                if row2 == direction and col1 == col2:
                    # attempt to move pawn 1 spot to empty square straight
                    return self.__check_for_check(to_move, move_to)
            if not Chess.__out_of_bounds((direction,)) and self._board[row2][col2]:
                # attempt to take piece diag
                if row2 == direction and (col2 == col1 - 1 or col2 == col1 + 1):
                    return self.__check_for_check(to_move, move_to)
            if not Chess.__out_of_bounds((direction,)) and not self._board[row2][col2]:
                if not self._enpassant:
                    return False
                if self._enpassant[0] != row1 or self._enpassant[1] != col2:
                    return False
                # attempt to en passant
                # check that move to is empty
                # then check that adjacent square is a pawn
                adjacent_pawn = self._board[row1][col2]
                if adjacent_pawn and adjacent_pawn.get_type() == Type.PAWN and self._enpassant[0]:
                  samecolor = adjacent_pawn.is_white() != piece_to_move.is_white()
                  if row2 == direction and (col2 == col1 - 1 or col2 == col1 + 1) and samecolor:
                    return self.__check_for_check(to_move, move_to)
            return False
        elif piece_to_move.get_type() == Type.ROOK:
            #Check for pieces in between
            #if piece inbetween target and piece, return false
            if row1 == row2:
                for i in range(col2 > col1 and col2-1 or col1-1, col1 if col2 > col1 else col2, -1):
                    if self._board[row1][i]:
                        return False
            elif col1 == col2:
                for i in range(row2 > row1 and row2-1 or row1-1, row1 if row2 > row1 else row2, -1):
                    if self._board[i][col1]:
                        return False
            else:
                return False
            # check that target spot has opposing piece in it or is empty
            if piece_to_remove and piece_to_remove.is_white() == piece_to_move.is_white():
                return False
            return self.__check_for_check(to_move, move_to)
        elif piece_to_move.get_type() == Type.KNIGHT:
            if abs(row1 - row2) == 2 and abs(col1 - col2) == 1:
                if piece_to_remove and piece_to_remove.is_white() != piece_to_move.is_white():
                    return self.__check_for_check(to_move,move_to)
                elif not piece_to_remove:
                    return self.__check_for_check(to_move,move_to)
                return False
            if abs(row1 - row2) == 1 and abs(col1 - col2) == 2:
                if piece_to_remove and piece_to_remove.is_white() != piece_to_move.is_white():
                    return self.__check_for_check(to_move,move_to)
                elif not piece_to_remove:
                    return self.__check_for_check(to_move,move_to)
                return False
        elif piece_to_move.get_type() == Type.BISHOP:
            dif_x = row1 - row2
            dif_y = col1 - col2
            #check that move_to is diag from to_move
            if abs(dif_x) != abs(dif_y):
                return False
            dif_x = dif_x/abs(dif_x) * -1
            dif_y = dif_y/abs(dif_y) * -1
            checkrow = row1 + int(math.floor(dif_x))
            checkcol = col1 + int(math.floor(dif_y))
            #check for no pieces en route to row2,col2
            move_one = False if checkrow == row2 and checkcol == col2 else True
            while not self.__out_of_bounds((checkrow, checkcol)) and move_one:
                to_check = self._board[checkrow][checkcol]
                if to_check:
                    return False
                checkrow += int(math.floor(dif_x))
                checkcol += int(math.floor(dif_y))
                if checkrow == row2 and checkcol == col2:
                    break
            #check row2,col2 for opp piece or free spot
            if piece_to_remove and piece_to_remove.is_white() != piece_to_move.is_white():
                return self.__check_for_check(to_move, move_to)
            elif not piece_to_remove:
                return self.__check_for_check(to_move, move_to)
            return False
        elif piece_to_move.get_type() == Type.QUEEN:
            #check rook style moves
            if row1 == row2:
                for i in range(col2 > col1 and col2-1 or col1-1, col1 if col2 > col1 else col2, -1):
                    if self._board[row1][i]:
                        return False
                if piece_to_remove and piece_to_remove.is_white() == piece_to_move.is_white():
                    return False
                return self.__check_for_check(to_move, move_to)
            elif col1 == col2:
                for i in range(row2 > row1 and row2-1 or row1-1, row1 if row2 > row1 else row2, -1):
                    if self._board[i][col1]:
                        return False
                if piece_to_remove and piece_to_remove.is_white() == piece_to_move.is_white():
                    return False
                return self.__check_for_check(to_move,move_to)
            #check bishop style moves
            dif_x = row1 - row2
            dif_y = col1 - col2
            if abs(dif_x) != abs(dif_y):
                return False
            dif_x = dif_x/abs(dif_x) * -1
            dif_y = dif_y/abs(dif_y) * -1
            checkrow = row1 + int(math.floor(dif_x))
            checkcol = col1 + int(math.floor(dif_y))
            #check for no pieces en route to row2,col2
            move_one = False if checkrow == row2 and checkcol == col2 else True
            while not self.__out_of_bounds((checkrow, checkcol)) and move_one:
                to_check = self._board[checkrow][checkcol]
                if to_check:
                    return False
                checkrow += int(math.floor(dif_x))
                checkcol += int(math.floor(dif_y))
                if checkrow == row2 and checkcol == col2:
                    break
            #check row2,col2 for opp piece or free spot
            if piece_to_remove and piece_to_remove.is_white() != piece_to_move.is_white():
                return self.__check_for_check(to_move, move_to)
            elif not piece_to_remove:
                return self.__check_for_check(to_move, move_to)
            return False
        elif piece_to_move.get_type() == Type.KING:
            #non-castle move logic:
            positions = ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(1,-1),(-1,1))
            for pos in positions:
                if row1 + pos[0] == row2 and col1 + pos[1] == col2:
                    return self.__check_for_check(to_move,move_to)
            #add castle logic here
            #King has moved, cant castle
            if piece_to_move.get_moved():
                return False
            #non-lateral movement, can't castle
            if row2 != row1:
                return False
            dir_x = (col1 - col2)/abs(col1-col2)*-1
            dir_x = int(math.floor(dir_x))
            #check that king is attempting to move 2 spots over
            if col1 + dir_x + dir_x != col2:
                return False
            #checkfor piece in way of castle move
            if self._board[row1][col1+dir_x]:
                return False
            if piece_to_remove:
                return False
            rook = None
            for i in range(col1+dir_x, -1 if dir_x == -1 else 8, dir_x):
                print('searching for rook @', row1, i)
                to_check = self._board[row1][i]
                if not to_check:
                    continue
                if to_check.get_type() != Type.ROOK:
                    return False
                if to_check.is_white() != piece_to_move.is_white():
                    return False
                rook = to_check
            if not rook:
                return False
            if rook.get_moved():
                return False
            #check that you can't castle through check
            self._board[row1][col1+dir_x] = piece_to_move
            self._board[row1][col1] = None
            check_flag = self.__in_check(self._turn)
            self._board[row1][col1] = piece_to_move
            self._board[row1][col1 + dir_x] = None
            if check_flag:
                return False
            #check that you aren't in check, cant castle out of check
            if self._turn:
                if self._game_state == State.WHITE_IN_CHECK or self._game_state == State.WHITE_CHECKMATED:
                    return False
            else:
                if self._game_state == State.BLACK_IN_CHECK or self._game_state == State.BLACK_CHECKMATED:
                    return False

            self._castle = True
            return self.__check_for_check(to_move,move_to)


    def __move_piece(self, to_move: tuple, move_to: tuple):
        # Assumes to_move can move to move_to
        # Completes the move with no data validation
        # Updates the gamestate after completing the move
        # Returns updated gamestate
        row1, col1 = to_move
        row2, col2 = move_to
        piece_to_move = self._board[row1][col1]
        piece_type = piece_to_move.get_type()
        if piece_type == Type.PAWN or piece_type == Type.ROOK:
            piece_to_move.move()
        #pawn moving diag to empty space means en passant
        if piece_type == Type.PAWN and not self._board[row2][col2]:
            if row1 - 1 == row2 and col1 - 1 == col2:
                self._board[row1][col1 - 1] = None
            elif row1 - 1 == row2 and col1 + 1 == col2:
                self._board[row1][col1 + 1] = None
            elif row1 + 1 == row2 and col1 + 1 == col2:
                self._board[row1][col1 + 1] = None
            elif row1 + 1 == row2 and col1 - 1 == col2:
                self._board[row1][col1 - 1] = None
        self._board[row2][col2] = piece_to_move
        self._board[row1][col1] = None
        self._turnNum += 1
        self._turn = not self._turn
        self.save_board()

        if piece_to_move.get_type() == Type.PAWN:
            if abs(row1 - row2) == 2:
                self._enpassant = move_to
            else:
                self._enpassant = None
        else:
            self._enpassant = None

        columncheck = (col1 + 2) == col2 or (col1 - 2) == col2
        if self._castle and piece_type == Type.KING and columncheck:
            dir_x = (col1 - col2)/abs(col1-col2)*-1
            dir_x = int(math.floor(dir_x))
            for i in range(col1+dir_x, -1 if dir_x == -1 else 8, dir_x):
                to_check = self._board[row1][i]
                if not to_check:
                    continue
                if to_check.get_type() == Type.ROOK:
                    print("Castle'd.")
                    to_check.move()
                    piece_to_move.move()
                    self._board[row1][col2-dir_x] = to_check
                    self._board[row1][i] = None
            self._castle = False
        else:
            self._castle = False

        # update the gamestate
        # check if one player is in check or checkmate
        if self.__in_check_mate(True) and self.__in_check_mate(False):
            self._game_state = State.STALEMATE
        elif self.__in_check_mate(True):
            self._game_state = State.WHITE_CHECKMATED
        elif self.__in_check_mate(False):
            self._game_state = State.BLACK_CHECKMATED
        elif self.__in_check(True):
            self._game_state = State.WHITE_IN_CHECK
        elif self.__in_check(False):
            self._game_state = State.BLACK_IN_CHECK
        elif piece_type == Type.PAWN and (row2 == 0 or row2 == 7):
            self._game_state = State.PROMOTION
        else:
            self._game_state = State.NORMAL
        print("Result state: ", self._game_state.name)

        return self._game_state.name # OUTPUT TO GUI


    def __check_for_check(self, to_move: tuple, move_to: tuple) -> bool:
        row1, col1 = to_move
        row2, col2 = move_to
        piece_to_move = self._board[row1][col1]
        piece_to_remove = self._board[row2][col2]
        self._board[row2][col2] = piece_to_move
        self._board[row1][col1] = None
        checked = self.__in_check(piece_to_move.is_white())
        self._board[row1][col1] = piece_to_move
        self._board[row2][col2] = piece_to_remove
        return not checked


    def __in_check(self, check_white: bool) -> bool:
        # Returns true/false based on self._board
        # if check_white then check if white is checked
        # if not check_white then check if black is checked

        # first find king position of type
        col_of_king, row_of_king = -1, -1
        for row_num, row in enumerate(self._board):
            for col_num, col in enumerate(row):
                if col == None:
                    continue
                elif col.get_type() == Type.KING and check_white == col.is_white():
                    col_of_king = col_num
                    row_of_king = row_num
                    break
            if col_of_king > -1:
                break

        # check if pawn rules can check
        to_check = None
        if check_white:
            checkrow = row_of_king - 1
            checkcol = col_of_king - 1
            to_check = not self.__out_of_bounds((checkrow,checkcol)) and self._board[checkrow][checkcol] or None
            if to_check:
                if to_check.get_type() == Type.PAWN and to_check.is_white() != check_white:
                    return True
            checkcol += 2
            to_check = not self.__out_of_bounds((checkrow,checkcol)) and self._board[checkrow][checkcol] or None
            if to_check:
                if to_check.get_type() == Type.PAWN and to_check.is_white() != check_white:
                    return True
        else:
            checkrow = row_of_king + 1
            checkcol = col_of_king -1
            to_check = not self.__out_of_bounds((checkrow,checkcol)) and self._board[checkrow][checkcol] or None
            if to_check:
                if to_check.get_type() == Type.PAWN and to_check.is_white() != check_white:
                    return True
            checkcol += 2
            to_check = not self.__out_of_bounds((checkrow,checkcol)) and self._board[checkrow][checkcol] or None
            if to_check:
                if to_check.get_type() == Type.PAWN and to_check.is_white() != check_white:
                    return True

        # check if rook rules can check (Queen as well)
        # checking the rows
        for checkrow in reversed(range(0, row_of_king)):
            to_check = self._board[checkrow][col_of_king]
            if to_check:
                if to_check.is_white() == check_white:
                    break
                elif to_check.get_type() == Type.ROOK or to_check.get_type() == Type.QUEEN:
                    return True
                else:
                    break
        for checkrow in range(row_of_king+1, 8):
            to_check = self._board[checkrow][col_of_king]
            if to_check:
                if to_check.is_white() == check_white:
                    break
                elif to_check.get_type() == Type.ROOK or to_check.get_type() == Type.QUEEN:
                    return True
                else:
                    break

        # checking the columns
        for checkcol in reversed(range(0, col_of_king)):
            to_check = self._board[row_of_king][checkcol]
            if to_check:
                if to_check.is_white() == check_white:
                    break
                elif to_check.get_type() == Type.ROOK or to_check.get_type() == Type.QUEEN:
                    return True
                else:
                    break
        for checkcol in range(col_of_king+1, 8):
            to_check = self._board[row_of_king][checkcol]
            if to_check:
                if to_check.is_white() == check_white:
                    break
                elif to_check.get_type() == Type.ROOK or to_check.get_type() == Type.QUEEN:
                    return True
                else:
                    break

        # check if bishop rules can check (Queen as well)
        positions = ((-1,1),(-1,-1),(1,-1),(1,1))
        for position in positions:
            checkrow = row_of_king + position[0]
            checkcol = col_of_king + position[1]
            while not self.__out_of_bounds((checkrow,checkcol)):
                to_check = self._board[checkrow][checkcol]
                if to_check:
                    if to_check.is_white() == check_white:
                        break
                    if to_check.get_type() == Type.BISHOP or to_check.get_type() == Type.QUEEN:
                        return True
                    else:
                        break
                checkrow += position[0]
                checkcol += position[1]

        # check if knight rules can check
        positions = [x for x in permutations((-2,2,-1,1),2) if abs(x[0]) != abs(x[1])]
        for position in positions:
            x = row_of_king + position[0]
            y = col_of_king + position[1]
            to_check = not self.__out_of_bounds((x,y)) and self._board[x][y] or None
            if not to_check:
                continue
            if to_check.get_type() == Type.KNIGHT and to_check.is_white() != check_white:
                return True

        return False


    def __in_check_mate(self, check_white: bool) -> bool:
        for i in range(8):
            for x in range(8):
                to_check = self._board[i][x]
                if to_check and to_check.is_white() == check_white:
                    if self.valid_moves((i,x)):
                        return False
        return True


    def save_board(self) -> bool:
        """()-> bool
        save current state of the board to the database
        returns bool depending on success
        """
        #enters a row into database for each piece on the board at this turnNum
        for row_num, row in enumerate(self._board):
            for col_num, col in enumerate(row):
                if not col:
                    continue
                moved = False
                pt = col.get_type()
                if pt == Type.PAWN or pt == Type.ROOK or pt == Type.KING:
                    moved = col.get_moved()
                if not db.saveState(str(col), col.is_white(), moved, row_num, col_num, self._turn, self._turnNum):
                    print("unable to save ", col, "@ ", row_num, col_num)
        print("Finished saving current board state")


    def load_board(self, turnNumber: int = -1) -> List[List[pieces.Piece]]:
        """(turnNumber: int)-> List[List[pieces.Piece]]
        returns a deepcopy of the present board
        Loads previous state of the board. Takes in one parameter, which is the
        turn number the player wishes to return to. Default is previous round.
        """
        #Cant use self. in default arg, so default arg is done below
        turnNumber = turnNumber if turnNumber > -1 else self._turnNum - 1
        dataList = db.loadState(turnNumber)
        tempBoard = [[None for _ in range(8)] for _ in range(8)]
        for dataSet in dataList:
            pieceName, col, moved, row, column, turnNum = dataSet
            if pieceName == "O":
                piece = pieces.Pawn(color = col)
                if moved:
                    piece.move()
            if pieceName == "B":
                piece = pieces.Bishop(color = col)
            if pieceName == "N":
                piece = pieces.Knight(color = col)
            if pieceName == "R":
                piece = pieces.Rook(color = col)
                if moved:
                    piece.move()
            if pieceName == "K":
                piece = pieces.King(color = col)
                if moved:
                    piece.move()
            if pieceName == "Q":
                piece = pieces.Queen(color = col)
            tempBoard[row][column] = piece
            self._turn = turnNum
        self._board = tempBoard
        self._turnNum = turnNumber


    @staticmethod
    def delete_saves() -> None:
        db.clearState()


    def board_to_string(self) -> str:
        """()-> str
        converts the board into a long string for servers. Towards the end,
        after the 'Z' letter, is the turnNum count and the current color's turn.
        """
        board = ""
        for row in self._board:
            for col in row:
                if not col:
                    board += "."
                else:
                    pt = col.get_type()
                    board += str(col)
                    board += "W" if col.is_white() else "U"
                    if pt == Type.PAWN or pt == Type.KING or pt == Type.ROOK:
                        if col.get_moved():
                            board += "X"
                        else:
                            board += "Y"
        board += "Z" + str(self._turnNum) + (self._turn and "E" or "L")
        return board


    def string_to_board(self, conv: str) -> None:
        """(conv: str)-> None
        imports a string usually resulted from board_to_string() to the Class'
        board, turnNum, and current player color. Saves the board to the database.
        """
        board = [[None for _ in range(8)] for _ in range(8)]
        i = x = 0
        start = conv[:conv.find("Z")]
        end = conv[conv.find("Z") + 1:]
        for z, let in enumerate(start):
            print(let, i, x)
            if let == "O":
                col = True if start[z+1] == "W" else False
                piece = pieces.Pawn(color = col)
                if start[z+2] == "X":
                    piece.move()
                board[i][x] = piece
            elif let == "B":
                col = True if start[z+1] == "W" else False
                piece = pieces.Bishop(color = col)
                board[i][x] = piece
            elif let == "N":
                col = True if start[z+1] == "W" else False
                piece = pieces.Knight(color = col)
                board[i][x] = piece
            elif let == "R":
                col = True if start[z+1] == "W" else False
                piece = pieces.Rook(color = col)
                if start[z+2] == "X":
                    piece.move()
                board[i][x] = piece
            elif let == "K":
                col = True if start[z+1] == "W" else False
                piece = pieces.King(color = col)
                if start[z+2] == "X":
                    piece.move()
                board[i][x] = piece
            elif let == "Q":
                col = True if start[z+1] == "W" else False
                piece = pieces.Queen(color = col)
                board[i][x] = piece
            if let != "X" and let != "Y" and let != "W" and let != "U":
                if x == 7:
                    x = 0
                    i += 1
                else:
                    x += 1
        self._board = board
        self._turnNum = int(end[:-1])
        self._turn = end[-1] == "E" and True or False
        self.save_board()


    @staticmethod
    def __out_of_bounds(bounds: tuple) -> bool:
        for bound in bounds:
            if bound < 0 or bound > 7:
                return True
        return False


    @staticmethod
    def get_starting_board() -> List[List[pieces.Piece]]:
        """()-> List[List[pieces.Piece]]
        generates the starting board for the class. Able to be called outside
        of the class when needed.
        """
        board = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            board[1][i] = pieces.Pawn(color=False)
            board[6][i] = pieces.Pawn(color=True)
        for i in range(4):
            piece_to_add = pieces.Rook(color=(i > 1 and True or False))
            board[i > 1 and 7 or 0][i % 2 and 7 or 0] = piece_to_add
        for i in range(4):
            piece_to_add = pieces.Knight(color=(i > 1 and True or False))
            board[i > 1 and 7 or 0][i % 2 and 6 or 1] = piece_to_add
        for i in range(4):
            piece_to_add = pieces.Bishop(color=(i > 1 and True or False))
            board[i > 1 and 7 or 0][i % 2 and 5 or 2] = piece_to_add
        board[0][3] = pieces.Queen(color=False)
        board[7][3] = pieces.Queen()
        board[0][4] = pieces.King(color=False)
        board[7][4] = pieces.King()
        return board
