import copy
from typing import List
import objects.chess.pieces as pieces
import objects.chess.dbms as db
from objects.chess.enums import PieceType as Type, GameState as State

# A Chess instance is a game of chess
# Game logic for new game:
# Create an instance of Chess
# user calls valid_move on a square
# valid move iterates over squares
# using can_move to check if the piece can_move there
#


class Chess:
    # TODO: add params to load a game, or function to load game
    def __init__(self) -> None:
        """
        Chess() -> initializes default chess game
        """
        self._board = Chess.get_starting_board()
        self._turn = True  # True indicates whether or not it's white's turn
        self._game_state = State.NORMAL
        self._turnNum = 0
        self.save_board()

    def attempt_move(self, to_move: tuple, move_to: tuple) -> State:
        """
        (tuple, tuple) -> State
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
        """(tuple) -> tuple
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
        row, col = to_move
        piece_to_move = self._board[row][col]

        if piece_to_move.get_type() == Type.PAWN:
            pass
        elif piece_to_move.get_type() == Type.ROOK:
            pass
        elif piece_to_move.get_type() == Type.BISHOP:
            pass
        elif piece_to_move.get_type() == Type.QUEEN:
            pass
        elif piece_to_move.get_type() == Type.KING:
            pass
        pass

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
            direction = piece_to_move.is_white() and row1 - 2 or row1 + 2
            if not piece_to_move.get_moved() and not Chess.__out_of_bounds((direction,)):
                if row2 == direction and col2 == col1 and not self._board[row2][col2]:
                    # attempt to move an unmoved pawn 2 spaces to an empty space
                    # modify board
                    return self.__check_for_check(to_move, move_to)
            direction = piece_to_move.is_white() and row1-1 or row1+1
            if not Chess.__out_of_bounds((direction,)) and not self._board[row2][col2]:
                if row2 == direction and col1 == col2:
                    # attempt to move pawn 1 spot to empty square straight
                    return self.__check_for_check(to_move, move_to)
            if not Chess.__out_of_bounds((direction,)) and self._board[row2][col2]:
                # attempt to take piece diag
                if row2 == direction and (col2 == col1 - 1 or col2 == col1 + 1):
                    return self.__check_for_check(to_move, move_to)
            if not Chess.__out_of_bounds((direction,)) and not self._board[row2][col2]:
                # attempt to en passant
                # check that move to is empty
                # then check that adjacent square isa  pawn
                adjacent_pawn = self._board[row1][col2]
                if adjacent_pawn and adjacent_pawn.get_type() == Type.PAWN:
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
            pass
        elif piece_to_move.get_type() == Type.QUEEN:
            pass
        elif piece_to_move.get_type() == Type.KING:
            pass

    def __move_piece(self, to_move: tuple, move_to: tuple) -> State:
        # Assumes to_move can move to move_to
        # Completes the move with no data validation
        # Updates the gamestate after completing the move
        # Returns updated gamestate
        row1, col1 = to_move
        row2, col2 = move_to
        piece_to_move = self._board[row1][col1]
        self._board[row2][col2] = piece_to_move
        self._board[row1][col1] = None
        self._turnNum += 1
        self.save_board()

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
        else:
            self._game_state = State.NORMAL

    def __check_for_check(self, to_move: tuple, move_to: tuple) -> bool:
        row1, col1 = to_move
        row2, col2 = move_to
        piece_to_move = self._board[row1][col1]
        self._board[row2][col2] = piece_to_move
        self._board[row1][col1] = None
        checked = self.__in_check(piece_to_move.is_white())
        if checked:
            self._board[row1][col1] = piece_to_move
            self._board[row2][col2] = None
            return False
        checked = self.__in_check_mate(piece_to_move.is_white())
        if checked:
            self._board[row1][col1] = piece_to_move
            self._board[row2][col2] = None
            return False
        self._board[row1][col1] = piece_to_move
        self._board[row2][col2] = None
        return True

    def __in_check(self, check_white: bool) -> bool:
        # Returns true/false based on self._board
        # if check_white then check if white is checked
        # if not check_white then check if black is checked

        # first find king position of type
        col_of_king, row_of_king = -1, -1
        for row_num, row in enumerate(self._board):
            for col_num, col in enumerate(row):
                if col == None:
                    break
                elif col.get_type() == Type.KING and check_white == col.is_white():
                    col_of_king = col_num
                    row_of_king = row_num
                    break
            if col_of_king > -1:
                break

        # check if pawn rules can check
        if check_white:
            checkrow = row_of_king - 1
            checkcol = col_of_king - 1
            if(self._board[checkrow][checkcol] != None):
                if(self._board[checkrow][checkcol].get_type() == Type.PAWN and
                 self._board[checkrow][checkcol].is_white() != check_white):
                    return True
            checkcol += 2
            if(self._board[checkrow][checkcol] != None):
                if(self._board[checkrow][checkcol].get_type() == Type.PAWN and
                 self._board[checkrow][checkcol].is_white() != check_white):
                    return True
        else:
            checkrow = row_of_king + 1
            checkcol = col_of_king - 1
            if(self._board[checkrow][checkcol] != None):
                if(self._board[checkrow][checkcol].get_type() == Type.PAWN and
                 self._board[checkrow][checkcol].is_white() != check_white):
                    return True
            checkcol += 2
            if(self._board[checkrow][checkcol] != None):
                if(self._board[checkrow][checkcol].get_type() == Type.PAWN and
                 self._board[checkrow][checkcol].is_white() != check_white):
                    return True

        # check if rook rules can check (Queen as well)
        # checking the rows
        for checkrow in reversed(range(0, row_of_king)):
            if(self._board[checkrow][col_of_king] != None):
                if(self._board[checkrow][col_of_king].is_white() == check_white):
                    break
                elif(self._board[checkrow][col_of_king].get_type() == Type.ROOK or
                 self._board[checkrow][col_of_king].get_type() == Type.QUEEN):
                    return True
                else:
                    break
        for checkrow in range(row_of_king + 1, 8):
            if(self._board[checkrow][col_of_king] != None):
                if(self._board[checkrow][col_of_king].is_white() == check_white):
                    break
                elif(self._board[checkrow][col_of_king].get_type() == Type.ROOK or
                 self._board[checkrow][col_of_king].get_type() == Type.QUEEN):
                    return True
                else:
                    break

        # checking the columns
        for checkcol in reversed(range(0, col_of_king)):
            if(self._board[row_of_king][checkcol] != None):
                if(self._board[row_of_king][checkcol].is_white() == check_white):
                    break
                elif(self._board[row_of_king][checkcol].get_type() == Type.ROOK or
                 self._board[row_of_king][checkcol].get_type() == Type.QUEEN):
                    return True
                else:
                    break
        for checkcol in range(col_of_king + 1, 8):
            if(self._board[row_of_king][checkcol] != None):
                if(self._board[row_of_king][checkcol].is_white() == check_white):
                    break
                elif(self._board[row_of_king][checkcol].get_type() == Type.ROOK or
                 self._board[row_of_king][checkcol].get_type() == Type.QUEEN):
                    return True
                else:
                    break

        # check if bishop rules can check (Queen as well)
        checkrow = row_of_king - 1
        checkcol = col_of_king + 1
        while(checkrow >= 0 and checkcol < 8):
            if(self._board[checkrow][checkcol] != None):
                if(self._board[checkrow][checkcol].is_white() == check_white):
                    break
                elif(self._board[checkrow][checkcol].get_type() == Type.BISHOP or
                 self._board[checkrow][checkcol].get_type() == Type.QUEEN):
                    return True
                else:
                    break
            checkrow -= 1
            checkcol += 1

        checkrow = row_of_king - 1
        checkcol = col_of_king - 1
        while(checkrow >= 0 and checkcol >= 0):
            if(self._board[checkrow][checkcol] != None):
                if(self._board[checkrow][checkcol].is_white() == check_white):
                    break
                elif(self._board[checkrow][checkcol].get_type() == Type.BISHOP or
                 self._board[checkrow][checkcol].get_type() == Type.QUEEN):
                    return True
                else:
                    break
            checkrow -= 1
            checkcol -= 1

        checkrow = row_of_king + 1
        checkcol = col_of_king + 1
        while(checkrow < 8 and checkcol < 8):
            if(self._board[checkrow][checkcol] != None):
                if(self._board[checkrow][checkcol].is_white() == check_white):
                    break
                elif(self._board[checkrow][checkcol].get_type() == Type.BISHOP or
                 self._board[checkrow][checkcol].get_type() == Type.QUEEN):
                    return True
                else:
                    break
            checkrow += 1
            checkcol += 1

        checkrow = row_of_king + 1
        checkcol = col_of_king - 1
        while(checkrow < 8 and checkcol >= 0):
            if(self._board[checkrow][checkcol] != None):
                if(self._board[checkrow][checkcol].is_white() == check_white):
                    break
                elif(self._board[checkrow][checkcol].get_type() == Type.BISHOP or
                 self._board[checkrow][checkcol].get_type() == Type.QUEEN):
                    return True
                else:
                    break
            checkrow += 1
            checkcol -= 1

        # check if knight rules can check
        if(row_of_king + 2 < 8 and col_of_king - 1 >= 0):
            x = row_of_king + 2
            y = col_of_king - 1
            if(self._board[x][y] != None):
                if(self._board[x][y].get_type() == Type.KNIGHT and self._board[x][y].is_white() != check_white):
                    return True
        if(row_of_king - 1 >= 0 and col_of_king + 2 < 8):
            x = row_of_king - 1
            y = col_of_king + 2
            if(self._board[x][y] != None):
                if(self._board[x][y].get_type() == Type.KNIGHT and self._board[x][y].is_white() != check_white):
                    return True
        if(row_of_king + 2 < 8 and col_of_king + 1 < 8):
            x = row_of_king + 2
            y = col_of_king + 1
            if(self._board[x][y] != None):
                if(self._board[x][y].get_type() == Type.KNIGHT and self._board[x][y].is_white() != check_white):
                    return True
        if(row_of_king + 1 < 8 and col_of_king + 2 < 8):
            x = row_of_king + 1
            y = col_of_king + 2
            if(self._board[x][y] != None):
                if(self._board[x][y].get_type() == Type.KNIGHT and self._board[x][y].is_white() != check_white):
                    return True
        if(row_of_king - 2 >= 0 and col_of_king - 1 >= 0):
            x = row_of_king - 2
            y = col_of_king - 1
            if(self._board[x][y] != None):
                if(self._board[x][y].get_type() == Type.KNIGHT and self._board[x][y].is_white() != check_white):
                    return True
        if(row_of_king - 1 >= 0 and col_of_king - 2 >= 0):
            x = row_of_king - 1
            y = col_of_king - 2
            if(self._board[x][y] != None):
                if(self._board[x][y].get_type() == Type.KNIGHT and self._board[x][y].is_white() != check_white):
                    return True
        if(row_of_king - 2 >= 0 and col_of_king + 1 < 8):
            x = row_of_king - 2
            y = col_of_king + 1
            if(self._board[x][y] != None):
                if(self._board[x][y].get_type() == Type.KNIGHT and self._board[x][y].is_white() != check_white):
                    return True
        if(row_of_king + 1 < 8 and col_of_king - 2 >= 0):
            x = row_of_king + 1
            y = col_of_king - 2
            if(self._board[x][y] != None):
                if(self._board[x][y].get_type() == Type.KNIGHT and self._board[x][y].is_white() != check_white):
                    return True

        return False

    def __in_check_mate(self, check_white: bool) -> bool:
        pass

    def save_board(self) -> bool:
        for row in range(8):
            for col in range(8):
                if self._board[row][col] != None:
                    if (db.saveState(self._board[row][col].__str__(), self._board[row][col].is_white(), self._board[row], self._board[col], self._turn, self._turnNum) == False):
                        print ("Board could not be saved successfully")
                        return False
        print ("Board saved successfully")
        return True

    def load_board(self, turnNumber = None) -> List[List[pieces.Piece]]:
    #Loads previous state of the board. Takes in one parameter, which is the turn number the player wishes to return to. Default is previous round.
        if turnNumber == None:
          turnNumber = self._turnNum - 1
        dataList = db.loadState(turnNumber)
        tempBoard = [[None for i in range(8)] for i in range(8)]
        for dataSet in dataList:
            pieceName, col, row, column = dataSet
            if pieceName == "O":
                piece = pieces.Pawn(color = col)
            elif pieceName == "B":
                piece = pieces.Bishop(color = col)
            elif pieceName == "N":
                piece = pieces.Knight(color = col)
            elif pieceName == "R":
                piece = pieces.Rook(color = col)
            elif pieceName == "K":
                piece = pieces.King(color = col)
            elif pieceName == "Q":
                piece = pieces.Queen(color = col)
            tempBoard[row][column] = piece
        return tempBoard

    @staticmethod
    def __out_of_bounds(bounds: tuple) -> bool:
        for bound in bounds:
            if bound < 0 or bound > 7:
                return True
        return False

    @staticmethod
    def get_starting_board() -> List[List[pieces.Piece]]:
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
