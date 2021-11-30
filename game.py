from objects import chess
import pygame as p
import client as cl
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

_CHESSBOARD_COLORS = [p.Color("white"), p.Color("gray"), p.Color("red")]

def loadChessImages():
    """ ()-> None
    this loads the image files correlated to chess. These images need to be stored in the
    resources/chess/ directory with the appropriately listed names.
    """
    pieces = [
        'bbishop', 'bking', 'bknight', 'bpawn', 'bqueen', 'brook',
        'wbishop', 'wking', 'wknight', 'wpawn', 'wqueen', 'wrook'
    ]
    for piece in pieces:
        _IMAGES[piece] = p.transform.scale(p.image.load("resources/chess/" + piece + ".png"), (_SQLEN, _SQLEN))

def drawChessGame(screen, game, playerMovement: list, validMoves: list = None):
    """ ()-> None
    general function to handle drawing for the ChessGame
    """
    board = game.get_board()
    drawChessScreen(screen)
    if len(playerMovement) > 0:
      highlightChessMovement(screen, game, playerMovement[0])
      if validMoves:
        for validMove in validMoves:
          highlightChessMovement(screen, game, validMove, True)
    drawChessPieces(screen, board)

def drawChessScreen(screen):
    """ ()-> None
    draws onto the screen the background of the chessboard with proper
    alternating colors
    """
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
    """ ()-> None
    draws onto the screen based on the ChessGame the selected piece and
    any other squares the way.
    """
    board = game.get_board()
    x,y = selectedSquare
    if board[x][y] != None or ignore:
      drawWhite = True
      for r in range(_DIMENSIONS):
        for c in range(_DIMENSIONS):
          if r==x and c==y:
            # red circle to highlight possible moves/selected piece
            p.draw.circle(screen, _CHESSBOARD_COLORS[3], (_SQLEN*c+(_SQLEN/2),_SQLEN*r+(_SQLEN/2)), _SQLEN/2)
            if drawWhite: # taken from drawing the chessboard, decides the color inner circle color
              color = _CHESSBOARD_COLORS[0]
            else:
              color = _CHESSBOARD_COLORS[1]
            # inner circle should match background square
            p.draw.circle(screen, color, (_SQLEN*c+(_SQLEN/2),_SQLEN*r+(_SQLEN/2)), _SQLEN/2.3)
          drawWhite = not drawWhite
        if r % 2 == 0:
          drawWhite = False
        else:
          drawWhite = True

def drawArrowPointers(screen, arrowsList: list):
    """ ()-> None
    draws arrow pointers for the player visualizing their strategy
    """
    pass

def drawChessPieces(screen, board):
    """ ()-> None
    this function draws to the screen the pieces present on the board found by
    the Chess() class
    """
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

def movePiece(game, playerMovement):
    board = game.get_board()
    x1,y1 = playerMovement[0]
    x2,y2 = playerMovement[1]

    if board[x1][y1] != None:
        game.attempt_move((x1,y1),(x2,y2))
        #game.__move_piece((x1,y1),(x2,y2))

def IngameMenu(screen, clock):
    """ ()-> None
    this function draws the in-game menu system to interact with
    """
    pass

# need some type of main function that runs in a loop with an exit condition
# pygame has an event logger and can interface with the exit button
def ChessGame(screen, clock):
    """ ()-> None
    this is the core process for the ChessGame
    """
    screen.fill(p.Color("white"))
    loadChessImages()
    p.display.set_caption("Chess")
    p.display.set_icon(_IMAGES['brook'])
    game = chess.Chess()  # need to initialize the game by calling the class
    session = True
    arrowsPointFlag = False
    _IN_GAME = True

    selectedSquare = ()     # need something to hold the selected spot on the GUI
    moveClicks = []       # need to keep track of the player clicks
    arrowClicks = []      # need to keep track of all of the arrows
    validMoves = []

    # game loop
    while session:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
#                    _IN_GAME = not _IN_GAME
                    _ON_MENU = not _ON_MENU
                elif event.key == p.K_LALT or event.key == p.R_ALT:
                    if arrowClicks:
                        arrowClicks.clear()
                        arrowsPointFlag = False
                elif event.key == p.K_RCTRL or event.key == p.K_LCTRL:
                    if arrowClicks and arrowClicks > 2: # pop the arrow
                        arrowClicks.pop(-2)
            elif event.type == p.MOUSEBUTTONDOWN and _IN_GAME:
                if event.button == 1 or event.button == 3:  # limits it to left and right mousebuttons
                    location = p.mouse.get_pos()
                    col,row = location
                    col = col // _SQLEN
                    row = row // _SQLEN

                    if selectedSquare == (row, col):
                        selectedSquare = ()
                        if moveClicks:        # to prevent any heinous bugs due to empty list
                            moveClicks.clear()
                        if arrowClicks:
                            arrowClicks.pop(-1)
                        if validMoves:
                            validMoves.clear()
                    else:
                        selectedSquare = (row, col)
                        if event.button == 1:
                            moveClicks.append(selectedSquare)
                        elif event.button == 3:
                            arrowClicks.append(selectedSquare)


                    if len(moveClicks) == 1:
                        tx,ty = moveClicks[0]
                    if game.get_board()[tx][ty] == None:
                        selectedSquare = ()
                        if moveClicks:
                            moveClicks.clear()
                        if validMoves:
                            validMoves.clear()
#                    else:
#                        validMoves = game.valid_moves(moveClicks[0])

                    print(f"Selected for movement: {selectedSquare}")

                    if len(moveClicks) == 2:
                        movePiece(game,moveClicks)
                        selectedSquare = ()
                        moveClicks.clear()
                        if validMoves:
                            validMoves.clear()

                    if len(arrowClicks) >= 2 and not arrowsPointFlag:
                        arrowsPointFlag = True


        if _IN_GAME:
            drawChessGame(screen, game, moveClicks, validMoves)
            if arrowsPointFlag:
                drawArrowPointers(screen, arrowClicks)
#        elif _ON_MENU:
#            IngameMenu(screen, clock)
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
