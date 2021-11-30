from objects import chess
import pygame as p
import sys

# knowing the width and height (pixel count/area of screen)
# dimensions of board is usually always 8
# need to know the length of the squares and something global to hold the images
# and probably a set FPS for drawing

_WIDTH = _HEIGHT = 512
_DIMENSIONS = 8
_SQLEN = _HEIGHT // _DIMENSIONS
_IMAGES = {}    # dictionary/hashmap. For quick image lookup
_MINFPS = 15
_MAXFPS = 30

_ON_MENU = False
_IN_GAME = False

_CHESSBOARD_COLORS = [p.Color("white"), p.Color("gray")]

# need to load the images
def loadImages():
    pieces = [
        'bbishop', 'bking', 'bknight', 'bpawn', 'bqueen', 'brook',
        'wbishop', 'wking', 'wknight', 'wpawn', 'wqueen', 'wrook'
    ]
    for piece in pieces:
        _IMAGES[piece] = p.transform.scale(p.image.load("resources/chess/" + piece + ".png"), (_SQLEN, _SQLEN))

# need to draw the game
def drawChessGame(screen, game, playerMovement: list, validMoves: list = None):
    board = game.get_board()
    drawChessScreen(screen)
    if len(playerMovement) > 0:
      highlightChessMovement(screen, game, playerMovement[0])
      if validMoves:
        for validMove in game.valid_moves(playerMovement[0]):
          highlightChessMovement(screen, game, validMove, True)
    drawChessPieces(screen, board)

def drawChessScreen(screen):
    drawWhite = True
    for r in range(_DIMENSIONS):
        for c in range(_DIMENSIONS):
            if drawWhite:
                p.draw.rect(screen, _CHESSBOARD_COLORS[0], [_SQLEN*c, _SQLEN*r, _SQLEN, _SQLEN])
            else:
                p.draw.rect(screen, _CHESSBOARD_COLORS[1], [_SQLEN*c, _SQLEN*r, _SQLEN, _SQLEN])
            drawWhite = not drawWhite
        if r % 2 == 0:
            drawWhite = False
        else:
            drawWhite = True

def highlightChessMovement(screen, game, selectedSquare, ignore: bool = False):
    board = game.get_board()
    x,y = selectedSquare
    if board[x][y] != None or ignore:
      drawWhite = True
      for r in range(_DIMENSIONS):
        for c in range(_DIMENSIONS):      
          if r==x and c==y:
            p.draw.circle(screen, p.Color("red"), (_SQLEN*c+(_SQLEN/2),_SQLEN*r+(_SQLEN/2)), _SQLEN/2)
            if drawWhite:
              color = _CHESSBOARD_COLORS[0]
            else:
              color = _CHESSBOARD_COLORS[1]
            p.draw.circle(screen, color, (_SQLEN*c+(_SQLEN/2),_SQLEN*r+(_SQLEN/2)), _SQLEN/2.3)
          drawWhite = not drawWhite
        if r % 2 == 0:
          drawWhite = False
        else:
          drawWhite = True

def drawChessPieces(screen, board):
    for row in range(_DIMENSIONS):
        for col in range(_DIMENSIONS):
            if board[row][col] != None: # always check if there's something there
                piece = board[row][col] # get the piece
                lookup = "" # initializes and clears the string

                if piece.is_white():    # if it's white, add "w"
                    lookup += "w"
                else:                   # otherwise it's black, add "b"
                    lookup += "b"

                # get the type name and lower string it
                lookup += str(piece.get_type().name).lower()

                # draw to the screen the piece, box it in as a rectangle
                screen.blit(_IMAGES[lookup], p.Rect(col*_SQLEN, row*_SQLEN, _SQLEN, _SQLEN))

def movePiece(game, playerMovment):
    board = game.get_board()
    x1,y1 = playerMovment[0]
    x2,y2 = playerMovment[1]

    if board[x1][y1] != None:
        game.attempt_move((x1,y1),(x2,y2))
        #game.__move_piece((x1,y1),(x2,y2))

def IngameMenu(screen, clock):
  pass

# need some type of main function that runs in a loop with an exit condition
# pygame has an event logger and can interface with the exit button
def ChessGame(screen, clock):
    screen.fill(p.Color("white"))
    loadImages()
    p.display.set_caption("Chess")
    p.display.set_icon(_IMAGES['brook'])
    game = chess.Chess()  # need to initialize the game by calling the class
    session = True
    _IN_GAME = True

    selectedSquare = ()     # need something to hold the selected spot on the GUI
    playerClicks = []       # need to keep track of the player clicks
    validMoves = []

    # game loop
    while session:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    pass
            elif event.type == p.MOUSEBUTTONDOWN and _IN_GAME:
                if event.button == 1 or event.button == 3:  # limits it to left and right mousebuttons
                    location = p.mouse.get_pos()
                    col,row = location
                    col = col // _SQLEN
                    row = row // _SQLEN
                
                    if selectedSquare == (row, col):
                        selectedSquare = ()
                        if playerClicks:        # to prevent any heinous bugs due to empty list
                            playerClicks.clear()
                        if validMoves:
                            validMoves.clear()
                    else:
                        selectedSquare = (row, col)
                        playerClicks.append(selectedSquare)

                    if len(playerClicks) == 1:
                        tx,ty = playerClicks[0]
                    if game.get_board()[tx][ty] == None:
                        selectedSquare = ()
                        if playerClicks:
                            playerClicks.clear()
                        if validMoves:
                            validMoves.clear()
                    else:
                        validMoves = game.valid_moves(playerClicks[0])

                    print(f"Selected: {selectedSquare}")

                    if len(playerClicks) == 2:
                        movePiece(game,playerClicks)
                        selectedSquare = ()
                        playerClicks.clear()
                        #validMoves.clear()

        drawChessGame(screen, game, playerClicks, validMoves)
        clock.tick(_MINFPS)
        p.display.flip()    # updates the screen

def MainMenu(screen, clock):
    while True:
        screen.fill((0,0,0))
        draw_text('')

if __name__ == "__main__":
    p.init()        # initialize pygame
    clock = p.time.Clock()
    screen = p.display.set_mode((_WIDTH, _HEIGHT))
    ChessGame(screen, clock) # main game for the board
    # will likely want to return to main menu of the whole game system
