import copy
from typing import List
import newPieces as pieces

#Once we get to the UI stages, this will make for very easy interaction
#The UI code will be responsible for displaying the UI
#Fetching the board and displaying it
#And converting mouse clicks to attempt_move


class Chess():
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
            return False
        if Chess.__out_of_bounds(row2) or Chess.__out_of_bounds(col2):
            return False
        piece_to_move = self._board[row1][col1]
        if not piece_to_move:
            return False
        if piece_to_move.is_white() != self._turn:
            return False
        
        #Check if the piece selected can move to the desired location
        #can_move will handle the brunt of the game logic
        if not self.__can_move(to_move, move_to):
            return False
        
        self.__move_piece(to_move, move_to)
        return True

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
        pass

    def __move_piece(self, to_move: tuple, move_to: tuple) -> None:
        #Returns 0 if the result of the move leaves the game in a stalemate
        #Returns 1 if the result of the move results in white in checkmate
        #Returns 2 if the result of the move results in black in checkmate
        #Returns 3 if the result of the move results in white in check
        #Returns 4 if the result of the move results in black in check
        #Returns 5 if the result of the move is normal play
        #Should probably just use enums for better legibility 
        pass

    @staticmethod
    def __out_of_bounds(num):
        #No reason to make this unique to an instance of the Chess class
        if num < 0 or num > 7:
            return True
        return False

    @staticmethod
    def get_starting_board() -> List[List[pieces.Piece]]:
        board = [None]*8
        for i in range(8):
            board[i] = [None]*8
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