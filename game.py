from objects import chess
from datetime import datetime
import random
import pygame as p
import client as cl
import math
import sys

# knowing the width and height (pixel count/area of screen)
# dimensions of board is usually always 8
# need to know the length of the squares and something global to hold the images
# and probably a set FPS for drawing
_FULLWIDTH = 896
_WIDTH = _HEIGHT = 512
_DIMENSIONS = 8
_SQLEN = _HEIGHT // _DIMENSIONS
_IMAGES = {}    # dictionary/hashmap. For quick image lookup
_MINFPS = 15
_MAXFPS = 30

_ON_MENU = False
_IN_GAME = False

_CHESSBOARD_COLORS = [p.Color("white"), p.Color("gray"), p.Color("red")]
_DROUGHT_COLORS = [p.Color("red"), p.Color("gray"), p.Color("white")]

def loadMenuImages():
    """ ()-> None
    this loads the image files correlated to the main menu. These images need to be stored in the resources/menu/ directory with the appropriately listed names.
    """
    mn = 'mainmenu_bg'
    _IMAGES[mn] = p.image.load("resources/menu/" + mn + ".png")

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
    colors = _CHESSBOARD_COLORS
    drawCheckeredBoard(screen,colors)
    if len(playerMovement) > 0:
      highlightPieceMovement(screen, game, colors, playerMovement[0])
      if validMoves:
        for validMove in validMoves:
          highlightPieceMovement(screen, game, colors, validMove, True)
    drawChessPieces(screen, board)
    #drawInGameMenu(screen, board)

def drawCheckeredBoard(screen, colors: list):
    """ ()-> None
    draws onto the screen the background of the board with alternating colors
    """
    alter = True    # offsets the next row and changes between one color and the next
    for r in range(_DIMENSIONS):
        for c in range(_DIMENSIONS):
            if alter:
                p.draw.rect(screen, colors[0], [_SQLEN*c, _SQLEN*r, _SQLEN, _SQLEN])
            else:
                p.draw.rect(screen, colors[1], [_SQLEN*c, _SQLEN*r, _SQLEN, _SQLEN])
            alter = not alter
        if r % 2 == 0:
            alter = False
        else:
            alter = True

def highlightPieceMovement(screen, game, colors: list, selectedSquare: tuple, ignore: bool = False):
    """ ()-> None
    draws onto the screen based on the ChessGame the selected piece and
    any other squares the way.
    """
    board = game.get_board()
    x,y = selectedSquare
    if board[x][y] != None or ignore:
      alter = True
      for r in range(_DIMENSIONS):
        for c in range(_DIMENSIONS):
          if r==x and c==y:
            # red circle to highlight possible moves/selected piece
            if not ignore:
              p.draw.circle(screen, colors[2], (_SQLEN*c+(_SQLEN/2),_SQLEN*r+(_SQLEN/2)), _SQLEN/2,2)
            else:
              p.draw.rect(screen, colors[2], [_SQLEN*c, _SQLEN*r, _SQLEN, _SQLEN],2)

            if alter: # taken from drawing the chessboard, decides the color inner circle color
              color = colors[0]
            else:
              color = colors[1]
            
            # inner circle should match background square
            if not ignore:
              p.draw.circle(screen, color, (_SQLEN*c+(_SQLEN/2),_SQLEN*r+(_SQLEN/2)), _SQLEN/2.3)

          alter = not alter
        if r % 2 == 0:
          alter = False
        else:
          alter = True

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
    print(playerMovement)

    if board[x1][y1] != None:
        state = game.attempt_move((x1,y1),(x2,y2))
        return state
        #game.__move_piece((x1,y1),(x2,y2))

def drawChessEndgame(screen, clock, game, result, player: int = 1):
    print(result)
    if result == "STALEMATE":
        result = "IT'S A TIE!"
    if result == "WHITE_CHECKMATED":
        result = "BLACK WINS!"
    if result == "BLACK_CHECKMATED":
        result = "WHITE WINS!" 

    result_button = p.Rect(_SQLEN * 8, 0, _SQLEN * 6, 50)
    count = 185
    rematch_button = p.Rect(_SQLEN * 9, count, _SQLEN * 4, 50)
    count += 55
    menu_button = p.Rect(_SQLEN * 9, count, _SQLEN * 4, 50)
    count += 55
    quit_button = p.Rect(_SQLEN * 9, count, _SQLEN * 4, 50)

    font = p.font.SysFont('Arial', 25)
    rematch = font.render("Rematch?", True, p.Color("white"))
    menu = font.render("Main Menu", True, p.Color("white"))
    quit = font.render("Quit", True, p.Color("white"))
    result = font.render(result,True,p.Color("white"))
    
    button_color = p.Color("black")
    
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = p.mouse.get_pos()
                    if rematch_button.collidepoint((x,y)):
                        print("Starting New Game")
                        if player == 1:
                            ChessGame(screen,clock,aimode=True)
                        if player == 2:
                            ChessGame(screen,clock)
                    if menu_button.collidepoint((x,y)):
                        print("Loading Main Menu")
                        MainMenu(p.display.set_mode((_WIDTH, _HEIGHT)), clock)
                    if quit_button.collidepoint((x,y)):
                        print("Quitting...")
                        p.quit()
                        sys.exit()
                        
        drawButton(screen, button_color, rematch, rematch_button)
        drawButton(screen, button_color, menu, menu_button)
        drawButton(screen, button_color, quit, quit_button)
        drawButton(screen, "red", result, result_button)
        
        clock.tick(_MINFPS)
        p.display.update()

# need some type of main function that runs in a loop with an exit condition
# pygame has an event logger and can interface with the exit button

def ChessGame(screen, clock, turn: int = None, aimode: bool = True, player: bool = False, secondplayer: bool = False, load: bool = False, multiplayer: bool = False):
    """ ()-> None
    this is the core process for the ChessGame
    """
    screen.fill(p.Color("white"))
    loadChessImages()
    p.display.set_caption("Chess")
    p.display.set_icon(_IMAGES['brook'])
    game = chess.Chess()    # need to initialize the game by calling the class
    if load:
      game.load_board(turn)
    else:
      game.delete_saves()
    session = True
    _IN_GAME = True

    selectedSquare = ()     # need something to hold the selected spot on the GUI
    moveClicks = []       # need to keep track of the player clicks
    validMoves = []
    state = None
    location = None

    if aimode:
      # Computer Player Movement
      random.seed(datetime.now())
      CPU_Pieces = []
      validCPUMoves = []
      captureMoves = []
      select = ()
         
    # game loop
    while session:
        if aimode and game.get_turn() != player:
            board = game.get_board() # Get updated board before each turn
            
            if _IN_GAME and not select:
                drawChessGame(screen, game, moveClicks, validCPUMoves) 
                InGameMenu(screen, clock, game._turn)
                if state == "STALEMATE" or state == "BLACK_CHECKMATED" or state == "WHITE_CHECKMATED":
                    drawChessEndgame(screen, clock, game, state)
                    
            clock.tick(_MINFPS)
            p.display.flip()    # updates the screen
            
            print("\nGetting CPU movable pieces...")
            for x in range(8):
                for y in range(8):
                    if board[x][y] != None:
                        if board[x][y]._color != player and game.valid_moves((x,y)):
                            CPU_Pieces.append((x,y))

            for x in range(len(CPU_Pieces)):
                selectedSquare = CPU_Pieces[x]
                validCPUMoves = game.valid_moves(selectedSquare)
                for y in range(len(validCPUMoves)):
                    x1,y1 = validCPUMoves[y]
                    if board[x1][y1] != None:
                        captureMoves.append(CPU_Pieces[x])
                        
            if captureMoves:
                print("CPU chooses to capture")
                select = random.randint(0,len(captureMoves)-1)
                selectedSquare = captureMoves[select]
            else:
                print("CPU chooses to move")
                select = random.randint(0,len(CPU_Pieces)-1)    
                selectedSquare = CPU_Pieces[select]
                
            moveClicks.append(selectedSquare)
            validCPUMoves = game.valid_moves(moveClicks[0])
            
            x1, y1 = moveClicks[0]
            print("Computer chose:", str(board[x1][y1]), "at",selectedSquare)
            
            if _IN_GAME:
                drawChessGame(screen, game, moveClicks, validCPUMoves) 
                InGameMenu(screen, clock, game._turn)
                if state == "STALEMATE" or state == "BLACK_CHECKMATED" or state == "WHITE_CHECKMATED":
                    drawChessEndgame(screen, clock, game, state)
                    
            clock.tick(_MINFPS)
            p.display.flip()    # updates the screen
            
            cl.time.sleep(1) # Allows time to see CPU selected piece
            
            captureMoves.clear() # To recieve movement of pieces that can capture
            
            for x in range(len(validCPUMoves)):
                x1, y1 = validCPUMoves[x]
                if board[x1][y1] != None:
                    captureMoves.append(validCPUMoves[x])
                             
            if captureMoves:
                print("CPU choosing capture move at random")
                print(captureMoves)
                select = random.randint(0,len(captureMoves)-1)
                selectedSquare = captureMoves[select]
            else:
                print("No capture moves for CPU")
                print(validCPUMoves)
                select = random.randint(0,len(validCPUMoves)-1)    
                selectedSquare = validCPUMoves[select]
                
            moveClicks.append(selectedSquare)
            print("CPU chose move:", moveClicks[1])
            
            state = movePiece(game,moveClicks)

            if len(moveClicks) == 2:
                selectedSquare = ()
                select = ()
                moveClicks.clear()
                validCPUMoves.clear()
                captureMoves.clear()
                CPU_Pieces.clear()

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
#                    _IN_GAME = not _IN_GAME
                    _ON_MENU = not _ON_MENU
            elif event.type == p.MOUSEBUTTONDOWN and _IN_GAME:
                if event.button == 1 or event.button == 3:  # limits it to left and right mousebuttons
                    location = p.mouse.get_pos()
                    col,row = location
                    col = col // _SQLEN
                    row = row // _SQLEN;

                    if selectedSquare == (row, col):
                        selectedSquare = ()
                        if moveClicks:        # to prevent any heinous bugs due to empty list
                            moveClicks.clear()
                        if validMoves:
                            validMoves.clear()
                    elif row < 8 and col < 8: # Only adds clicks that are on gameboard
                        selectedSquare = (row, col)
                        moveClicks.append(selectedSquare)
                    else:
                        continue
                    
                    if len(moveClicks) == 1:
                        tx,ty = moveClicks[0]

#                    if ty < 8:		# Only checks clicks that are on gameboard
                    if game.get_board()[tx][ty] == None:
                        selectedSquare = ()
                        if moveClicks:
                            moveClicks.clear()
                        if validMoves:
                            validMoves.clear()
                    elif moveClicks:
                        validMoves = game.valid_moves(moveClicks[0])

                        print(f"Selected for movement: {selectedSquare}")

                    if len(moveClicks) == 2:
                        state = movePiece(game,moveClicks)
                        selectedSquare = ()
                        moveClicks.clear()
                        validMoves.clear()

        if _IN_GAME:
            drawChessGame(screen, game, moveClicks, validMoves) 
            InGameMenu(screen, clock, game._turn)
            if state == "STALEMATE" or state == "BLACK_CHECKMATED" or state == "WHITE_CHECKMATED":
                drawChessEndgame(screen, clock, game, state, 2)
            # p.display.set_mode((_WIDTH-256, _HEIGHT))
#        elif _ON_MENU:
#            IngameMenu(screen, clock)
        clock.tick(_MINFPS)
        p.display.flip()    # updates the screen
        
# MENU UTILITIES ----------------------------------------------------------------------------------

def drawButton(screen, color, ren, button):
    draw = p.draw.rect(screen, color, button)
    loc = ren.get_rect(center = draw.center)
    screen.blit(ren, loc)

# MENUS -------------------------------------------------------------------------------------------

def InGameMenu(screen, clock, _turn):
    """ ()-> None
    this function draws the in-game menu system to interact with
    """
    turnText = "white" if _turn else "black"
    turnFill = "white" if not _turn else "black"
    
    info = p.Surface((384,384))
    info.fill(p.Color(240,234,214))
    menu = p.Surface((384,128))
    menu.fill(p.Color(255,204,203))
    screen.blit(info,(512,0))
    screen.blit(menu,(512,384))
    
    count = 416
    
    turn_button = p.Rect(_SQLEN * 8, 0, _SQLEN * 6, 30)
    quit_button = p.Rect(_SQLEN * 8 + 5, count, _SQLEN * 3 - 10, 50)
    save_button = p.Rect(_SQLEN * 11 + 5, count, _SQLEN * 3 - 10, 50)

    font = p.font.SysFont('Arial', 25)
    quit = font.render("Quit", True, p.Color("white"))
    save = font.render("Save", True, p.Color("white"))
    turn = font.render("White Turn" if _turn else "Black Turn", True, p.Color(turnText))
    
    drawButton(screen, "red", quit, quit_button)
    drawButton(screen, "red", save, save_button)
    drawButton(screen, turnFill, turn, turn_button)
    
def PlayerOptionMenu(screen, clock):
    """ ()-> None
    this function draws the in-game menu system to interact with
    """    
    choice_button = p.Rect(_SQLEN, 150, _SQLEN * 6, 50)
    white_button = p.Rect(_SQLEN * 2, 205, _SQLEN * 4, 50)
    black_button = p.Rect(_SQLEN * 2, 260, _SQLEN * 4, 50)
    back_button = p.Rect(_SQLEN * 2, 315, _SQLEN * 4, 50)

    font = p.font.SysFont('Arial', 25)
    choice = font.render("Choose color to control", True, p.Color("white"))
    white = font.render("White", True, p.Color("white"))
    black = font.render("Black", True, p.Color("white"))
    back = font.render("Main Menu", True, p.Color("white"))

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = p.mouse.get_pos()
                    if white_button.collidepoint((x,y)):
                        print("Player is White")
                        #screen, clock, turn: int = None, load: bool = False, player: bool = False
                        ChessGame(p.display.set_mode((_FULLWIDTH, _HEIGHT)),clock,turn = None,aimode = True,load = False,player = True)
                    if black_button.collidepoint((x,y)):
                        print("Player is Black")
                        ChessGame(p.display.set_mode((_FULLWIDTH, _HEIGHT)),clock,turn = None,aimode = True,load = False,player = False)
                    if back_button.collidepoint((x,y)):
                        print("Back to Main Menu")
                        MainMenu(screen,clock)
    
        screen.fill(p.Color("gray"))
        
        drawButton(screen, "black", choice, choice_button)
        drawButton(screen, "red", white, white_button)
        drawButton(screen, "red", black, black_button)
        drawButton(screen, "red", back, back_button)
    
        clock.tick(_MINFPS)
        p.display.update()
    
def playMenuOptions():
    # draws the options between singleplayer against AI vs another player on a local machine

# this will be opened first, and it's what will call the game to run.
def MainMenu(screen, clock):
    count = 100
    single_button = p.Rect(_SQLEN * 2, count, _SQLEN * 4, 50)
    count += 100
    play_button = p.Rect(_SQLEN * 2, count, _SQLEN * 4, 50)
    #count += 100
    #multi_button = p.Rect(_SQLEN * 2, 200, _SQLEN * 4, 50)
    count += 100
    load_button = p.Rect(_SQLEN * 2, count, _SQLEN * 4, 50)
    count += 100
    quit_button = p.Rect(_SQLEN * 2, count, _SQLEN * 4, 50)

    font = p.font.SysFont('Arial', 25)
    single = font.render("Single Player Game", True, p.Color("white"))
    play = font.render("Two Player Game", True, p.Color("white"))
    #multi = font.render("Play Multiplayer", True, p.Color("white"))
    load = font.render("Load Previous", True, p.Color("white"))
    quit = font.render("Quit", True, p.Color("white"))

    button_color = p.Color("red")

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = p.mouse.get_pos()
                    if single_button.collidepoint((x,y)):
                        print("Selecting color to control")
                        PlayerOptionMenu(screen,clock)
                    if play_button.collidepoint((x,y)):
                        print("Starting New Two Player Game")
                        ChessGame(p.display.set_mode((_FULLWIDTH, _HEIGHT)),clock) # _FULLWIDTH
                    #if multi_button.collidepoint((x,y)):
                    #    print("Starting Multiplayer Session")
                    #    ChessGame(screen,clock, multiplayer = True)
                    if load_button.collidepoint((x,y)):
                        print("Loading Previous Session")
                        inturn = int(input("Input Turn Number : "))
                        ChessGame(p.display.set_mode((_FULLWIDTH, _HEIGHT)),clock, turn = inturn, load = True)
                    if quit_button.collidepoint((x,y)):
                        print("Quitting...")
                        p.quit()
                        sys.exit()


        #screen.blit(_IMAGES['mainmenu_background'], (0,0))
        screen.fill(p.Color("gray"))

        drawButton(screen, button_color, single, single_button)
        drawButton(screen, button_color, play, play_button)
        #drawButton(screen, button_color, multi, multi_button)
        drawButton(screen, button_color, load, load_button)
        drawButton(screen, button_color, quit, quit_button)

        clock.tick(_MINFPS)
        p.display.update()

if __name__ == "__main__":
    p.init()        # initialize pygame
    clock = p.time.Clock()
    screen = p.display.set_mode((_WIDTH, _HEIGHT))
    #ChessGame(screen, clock) # main game for the board
    MainMenu(screen,clock)
    # will likely want to return to main menu of the whole game system
