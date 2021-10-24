
import copy
from typing import List
import newPieces as pieces
from enums import PieceType as Type, GameState as State

#A Chess instance is a game of chess
#Game logic for new game:
#Create an instance of Chess
#user calls valid_move on a square
#valid move iterates over squares
#using can_move to check if the piece can_move there
#


class Chess:
    #TODO: add params to load a game, or function to load game
    def __init__(self) -> None:
        """
        Chess() -> initializes default chess game
        """
        self._board = Chess.get_starting_board()
        self._turn = True #True indicates whether or not it's white's turn
        self._game_state = State.NORMAL
    
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
        row1,col1 = to_move
        row2,col2 = move_to
        #validate data passed:
        #Check that locations passed are vald
        if Chess.__out_of_bounds((row1,col1,row2,col2)):
            return self._game_state
        piece_to_move = self._board[row1][col1]
        #Check for a piece to move at to_move
        if not piece_to_move:
            return self._game_state
        if piece_to_move.is_white() != self._turn:
            return self._game_state
        #Check for actual move attempt
        if to_move == move_to:
            return self._game_state
        
        #Check if the piece selected can move to the desired location
        #can_move will handle the brunt of the game logic
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
        #Returns a tuple of tuples
        #Each tuple is a row,col to which the piece located @to_move may move to
        #returns empty tuple if no valid moves available, or invalid input
        #Easiest way I think would be validating to_move and then calling can_move on all squares
        #index and return any that return true, although that may prove inefficient
        row,col = to_move
        piece_to_move = self._board[row][col]

        if(piece_to_move.get_type() == Type.PAWN):

        elif(piece_to_move.get_type() == Type.ROOK):

        elif(piece_to_move.get_type() == Type.BISHOP):

        elif(piece_to_move.get_type() == Type.QUEEN):

        elif(piece_to_move.get_type() == Type.KING):

        pass

    def get_board(self) -> List[List[pieces.Piece]]:
        """()-> List[List[pieces.Piece]
        returns a deepcopy of the present board
        """
        #return copy of list to prevent modification
        #if anyone knows a less costly way of returning a copy
        #of the list, then please implement it, not that this
        #will really affect us here, I'd just be curious to know in general
        return copy.deepcopy(self._board)

    def get_turn(self) -> bool:
        """() -> bool
        returns True if white's turn, False if black
        """
        return self._turn

    def __can_move(self, to_move: tuple, move_to: tuple) -> bool:
        #Assumes that to_move and move_to are in bounds
        #For bug prevention, any variations to the given bounds
        #Will get validated before accessing
        row1,col1 = to_move
        row2,col2 = move_to
        piece_to_move = self._board[row1][col1]
        
        #Cannot land on own piece ever, right?
        piece_to_remove = self._board[row2][col2]
        if piece_to_remove and piece_to_remove.is_white() == piece_to_move.is_white():
            return False

        #Cannot move to own spot
        if to_move == move_to: 
            return False

        #Get the piece at to_move, then branch to if statements based on piece
        if piece_to_move.get_type() == Type.PAWN:
            #a pawn may move 2 spaces if not yet moved
            #one space forward anytime
            #diag to take an occupied opp
            #diag to take an empty spot if adjacent is opp pawn (en passant)
            direction = piece_to_move.is_white() and row1 - 2 or row1 + 2
            if not piece_to_move.get_moved() and not Chess.__out_of_bounds((direction,)):
                if row2 == direction and col2 == col1 and not self._board[row2][col2]:
                    #attempt to move an unmoved pawn 2 spaces to an empty space
                    #modify board
                    return self.__check_for_check(to_move, move_to)
            direction = piece_to_move.is_white() and row1-1 or row1+1
            if not Chess.__out_of_bounds((direction,)) and not self._board[row2][col2]:
                if row2 == direction and col1 == col2:
                    #attempt to move pawn 1 spot to empty square straight
                    return self.__check_for_check(to_move, move_to)
            if not Chess.__out_of_bounds((direction,)) and self._board[row2][col2]:
                #attempt to take piece diag
                if row2 == direction and (col2 == col1 - 1 or col2 == col1 + 1):
                    return self.__check_for_check(to_move, move_to)
            if not Chess.__out_of_bounds((direction,)) and not self._board[row2][col2]:
                #attempt to en passant
                #check that move to is empty
                #then check that adjacent square isa  pawn
                adjacent_pawn = self._board[row1][col2]
                if adjacent_pawn and adjacent_pawn.get_type() == Type.PAWN:
                    return self.__check_for_check(to_move, move_to)
            return False
        elif piece_to_move.get_type() == Type.ROOK:
          pass
        elif piece_to_move.get_type() == Type.BISHOP:
          pass
        elif piece_to_move.get_type() == Type.QUEEN:
          pass
        elif piece_to_move.get_type() == Type.KING:
          pass


    def __move_piece(self, to_move: tuple, move_to: tuple) -> None:
        #Assumes to_move can move to move_to
        #Completes the move with no data validation
        #Updates the gamestate after completing the move
        #Returns updated gamestate
        row1,col1 = to_move
        row2,col2 = move_to
        piece_to_move = self._board[row1][col1]
        self._board[row2][col2] = piece_to_move
        self._board[row1][col1] = None

        #update the gamestate
        #check if one player is in check or checkmate
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
        row1,col1 = to_move
        row2,col2 = move_to
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
        #Returns true/false based on self._board
        #if check_white then check if white is checked
        #if not check_white then check if black is checked
        
        #first find king position of type
        col_of_king,row_of_king = -1,-1
        for row in range(0,8):
          for col in range(0,8):
            if(self._board[row][col] != None):
              if(self._board[row][col].get_type() == Type.KING and check_white == board[row][col].is_white()):
                row_of_king = row
                col_of_king = col
                break
          if(col_of_king >= 0 and row_of_king >= 0):
            break

        #check if pawn rules can check

        #check if rook rules can check

        #check if bishop rules can check

        #check if queen rules can check
        #might be able to combine it with rook and bishop rules
        pass

    def __in_check_mate(self, check_white: bool) -> bool:
        pass

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
            board[1][i] = pieces.Pawn(color = False)
        for i in range(8):
            board[6][i] = pieces.Pawn()
        for i in range(4):
            piece_to_add = pieces.Rook(color = (i > 1 and True or False))
            board[i > 1 and 7 or 0][i % 2 and 7 or 0] = piece_to_add
        for i in range(4):
            piece_to_add = pieces.Knight(color = (i > 1 and True or False))
            board[i > 1 and 7 or 0][i % 2 and 6 or 1] = piece_to_add
        for i in range(4):
            piece_to_add = pieces.Bishop(color = (i > 1 and True or False))
            board[i > 1 and 7 or 0][i % 2 and 5 or 2] = piece_to_add
        board[0][3] = pieces.Queen(color = False)
        board[7][3] = pieces.Queen()
        board[0][4] = pieces.King(color = False)
        board[7][4] = pieces.King()
        return board