import copy
from typing import List
import newPieces as pieces

#Once we get to the UI stages, this will make for very easy interaction
#The UI code will be responsible for displaying the UI
#Fetching the board and displaying it
#And converting mouse clicks to attempt_move


class Chess:
    #Can expand upon this later to take arguments to load a game
    #Load a game w/board + whose turn, anymore info needed?
    #Reference: self._board[row][col]
    def __init__(self) -> None:
        self._board = Chess.get_starting_board()
        self._turn = True #True indicates whether or not it's white's turn
    
    def attempt_move(self, to_move: tuple, move_to: tuple) -> int:
        #to_move and move_to are tuples of 2 ints 0-7 inclusive
        #Returns -1 for invalid input/unable to move piece
        #Otherwise, returns an integer (the return valud of __move_piece)
        #Representing the resulting game state after the move

        row1,col1 = to_move
        row2,col2 = move_to
        #validate data passed:
        if Chess.__out_of_bounds(row1) or Chess.__out_of_bounds(col1):
            return -1
        if Chess.__out_of_bounds(row2) or Chess.__out_of_bounds(col2):
            return -1
        piece_to_move = self._board[row1][col1]
        if not piece_to_move:
            return -1
        if piece_to_move.is_white() != self._turn:
            return -1
        if to_move == move_to:
            return -1
        
        #Check if the piece selected can move to the desired location
        #can_move will handle the brunt of the game logic
        if not self.__can_move(to_move, move_to):
            return -1
        
        return self.__move_piece(to_move, move_to)
        

    def valid_moves(self, to_move: tuple) -> tuple:
        #Returns a tuple of tuples
        #Each tuple is a row,col to which the piece located @to_move may move to
        #returns empty tuple if no valid moves available, or invalid input
        #Easiest way I think would be validating to_move and then calling can_move on all squares
        #index and return any that return true, although that may prove inefficient
        pass

    def get_board(self) -> List[List[pieces.Piece]]:
        #return copy of list to prevent modification
        #if anyone knows a less costly way of returning a copy
        #of the list, then please implement it, not that this
        #will really affect us here, I'd just be curious to know in general
        return copy.deepcopy(self._board)

    def __can_move(self, to_move: tuple, move_to: tuple) -> bool:
        #Data passed should already be validated, but it doesn't hurt to validate again
        row1,col1 = to_move
        row2,col2 = move_to
        if Chess.__out_of_bounds(row1) or Chess.__out_of_bounds(col1):
            return False
        if Chess.__out_of_bounds(row2) or Chess.__out_of_bounds(col2):
            return False
        piece_to_move = self._board[row1][col1]
        if not piece_to_move:
            return False
        #Don't check turns here, leaves the function open for more usage
        #Cannot land on own piece ever, right?
        piece_to_remove = self._board[row2][col2]
        if piece_to_remove and piece_to_remove.is_white() and piece_to_move.is_white():
            return False
        if piece_to_remove and (not piece_to_remove.is_white()) and (not piece_to_move.is_white()):
            return False
        #Cannot move to own spot
        if to_move == move_to: 
            return False

        #Get the piece at to_move, then branch to if statements based on piece
        if piece_to_move.get_type() == pieces.Type.PAWN:
            #a pawn may move 2 spaces if not yet moved
            #one space forward anytime
            #diag to take an occupied opp
            #diag to take an empty spot if adjacent is opp pawn (en passant)
            direction = piece_to_move.is_white() and row1 - 2 or row1 + 2
            if (not piece_to_move.get_moved()) and not Chess.__out_of_bounds(direction):
                if row2 == direction and col2 == col1 and not self._board[row2][col2]:
                    #attempt to move an unmoved pawn 2 spaces
                    #modify board
                    self._board[row2][col2] = piece_to_move
                    self._board[row1][col1] = None
                    #check if your own move puts you in check/checkmate
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



    def __move_piece(self, to_move: tuple, move_to: tuple) -> None:
        #Returns 0 if the result of the move leaves the game in a stalemate
        #Returns 1 if the result of the move results in white in checkmate
        #Returns 2 if the result of the move results in black in checkmate
        #Returns 3 if the result of the move results in white in check
        #Returns 4 if the result of the move results in black in check
        #Returns 5 if the result of the move is normal play
        #Should probably just use enums for better legibility 
        pass

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
        pass

    def __in_check_mate(self) -> bool:
        pass

    @staticmethod
    def __out_of_bounds(num):
        #No reason to make this unique to an instance of the Chess class
        if num < 0 or num > 7:
            return True
        return False

    @staticmethod
    def get_starting_board() -> List[List[pieces.Piece]]:
        board = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            board[1][i] = pieces.Pawn(pieces.Type.PAWN, color = False)
        for i in range(8):
            board[6][i] = pieces.Pawn(pieces.Type.PAWN)
        board[0][0] = pieces.Rook(pieces.Type.ROOK, color = False)
        board[0][7] = pieces.Rook(pieces.Type.ROOK, color = False)
        board[7][0] = pieces.Rook(pieces.Type.ROOK)
        board[7][7] = pieces.Rook(pieces.Type.ROOK)
        board[0][1] = pieces.Knight(pieces.Type.KNIGHT, color = False)
        board[0][6] = pieces.Knight(pieces.Type.KNIGHT, color = False)
        board[7][6] = pieces.Knight(pieces.Type.KNIGHT)
        board[7][1] = pieces.Knight(pieces.Type.KNIGHT)
        board[0][2] = pieces.Bishop(pieces.Type.BISHOP, color = False)
        board[0][5] = pieces.Bishop(pieces.Type.BISHOP, color = False)
        board[7][2] = pieces.Bishop(pieces.Type.BISHOP)
        board[7][5] = pieces.Bishop(pieces.Type.BISHOP)
        board[0][3] = pieces.Queen(pieces.Type.QUEEN, color = False)
        board[7][3] = pieces.Queen(pieces.Type.QUEEN)
        board[0][4] = pieces.King(pieces.Type.KING, color = False)
        board[7][4] = pieces.King(pieces.Type.KING)
        return board