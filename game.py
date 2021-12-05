from objects import chess
from datetime import datetime
import random
import pygame as p
import client as cl
import sys
import time

from objects.chess.chess import Chess

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
    this loads the image files correlated to the main menu. These images need to
    be stored in the resources/menu/ directory with the appropriately listed names.
    """
    ims = ['mainmenu_bg', 'icon']
    for im in ims:
        _IMAGES[im] = p.image.load("resources/menu/" + im + ".png")


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


# DRAW FUNCTIONS ---------------------------------------------------------------

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


def drawChessEndgame(screen, clock, game, result, player: int = 1):
    """ ()-> None
    this function draws to the screen the pieces end results screen
    """
    print(result)
    if result == "STALEMATE":
        result = "IT'S A TIE!"
    if result == "WHITE_CHECKMATED":
        result = "BLACK WINS!"
    if result == "BLACK_CHECKMATED":
        result = "WHITE WINS!"

    result_label = p.Rect(_SQLEN * 8, 0, _SQLEN * 6, 50)
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

    session = True

    while session:
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
                            session = False
                            ChessGame(screen,clock,aimode=True)
                        if player == 2:
                            session = False
                            ChessGame(screen,clock)
                    if menu_button.collidepoint((x,y)):
                        print("Loading Main Menu")
                        session = False
                        MainMenu(p.display.set_mode((_WIDTH, _HEIGHT)), clock)
                    if quit_button.collidepoint((x,y)):
                        print("Quitting...")
                        session = False
                        p.quit()
                        sys.exit()

        info = p.Surface((384,512))
        info.fill(p.Color(240,234,214))
        screen.blit(info,(512,0))

        drawButton(screen, button_color, rematch, rematch_button)
        drawButton(screen, button_color, menu, menu_button)
        drawButton(screen, button_color, quit, quit_button)
        drawButton(screen, "red", result, result_label)

        clock.tick(_MINFPS)
        p.display.update()


# PIECE MANIPULATION -----------------------------------------------------------

def movePiece(game, playerMovement):
    board = game.get_board()
    x1,y1 = playerMovement[0]
    x2,y2 = playerMovement[1]
    print(playerMovement)

    if board[x1][y1] != None:
        #print("Before:\n" + str(game))
        state = game.attempt_move((x1,y1),(x2,y2))
        #print("After:\n" + str(game))
        return state


def promotePawn(screen, game, playerMovement):
    print("Trying to promote piece at:", playerMovement)
    pieceType = None

    count = 100
    rook_button = p.Rect(_SQLEN * 9, count, _SQLEN * 4, 50)
    count += 55
    knight_button = p.Rect(_SQLEN * 9, count, _SQLEN * 4, 50)
    count += 55
    bishop_button = p.Rect(_SQLEN * 9, count, _SQLEN * 4, 50)
    count += 55
    queen_button = p.Rect(_SQLEN * 9, count, _SQLEN * 4, 50)

    font = p.font.SysFont('Arial', 25)
    rook= font.render("Rook", True, p.Color("white"))
    knight = font.render("Knight", True, p.Color("white"))
    bishop = font.render("Bishop", True, p.Color("white"))
    queen = font.render("Queen", True, p.Color("white"))

    session = True
    while session:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = p.mouse.get_pos()
                    if rook_button.collidepoint((x,y)):
                        session = False
                        pieceType = "ROOK"
                    if knight_button.collidepoint((x,y)):
                        session = False
                        pieceType = "KNIGHT"
                    if bishop_button.collidepoint((x,y)):
                        session = False
                        pieceType = "BISHOP"
                    if queen_button.collidepoint((x,y)):
                        session = False
                        pieceType = "QUEEN"

        drawButton(screen, "black", rook, rook_button)
        drawButton(screen, "black", knight, knight_button)
        drawButton(screen, "black", bishop, bishop_button)
        drawButton(screen, "black", queen, queen_button)

        clock.tick(_MINFPS)
        p.display.update()

    return game.promote(playerMovement, pieceType)


# CORE GAME --------------------------------------------------------------------

# need some type of main function that runs in a loop with an exit condition
# pygame has an event logger and can interface with the exit button

def ChessGame(screen, clock, turn: int = None, aimode: bool = False,
            player: bool = False, secondplayer: bool = False, load: bool = False,
            multiplayer: bool = False):
    """ ()-> None
    this is the core process for the ChessGame
    """
    screen.fill(p.Color("white"))

    loadChessImages()
    game = chess.Chess()    # need to initialize the game by calling the class
    pt = 0
    client = None
    if multiplayer:
        client = cl.Client()
        pt = client.color
        print("Pt is ", pt)
    if load:
        game.load_board(turn)
    else:
        game.delete_saves()
    session = True
    _IN_GAME = True

    selectedSquare = ()  # need something to hold the selected spot on the GUI
    promote = ()         # Used for promotion
    moveClicks = []      # need to keep track of the player clicks
    validMoves = []      # used to hold valid moves
    state = None         # gamestate
    location = None      # mouse pointer location

    if aimode:
      # Computer Player Movement
      random.seed(datetime.now())
      CPU_Pieces = []
      validCPUMoves = []
      captureMoves = []
      select = ()

    drawChessGame(screen, game, moveClicks, validMoves)
    quit_button = InGameMenu(screen, clock, game._turn)

    # game loop
    while session:
          if aimode and game.get_turn() != player:
            board = game.get_board() # Get updated board before each turn

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

            time.sleep(1) # Allows time to see CPU selected piece

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

            if state == "PROMOTION":
                x, y = moveClicks[1]
                print("CPU promotes pawn to queen")
                state = game.promote((x,y), "QUEEN")
                promote = ()

            if len(moveClicks) == 2:
                selectedSquare = ()
                select = ()
                moveClicks.clear()
                validCPUMoves.clear()
                captureMoves.clear()
                CPU_Pieces.clear()

          else:
            for event in p.event.get():
                if event.type == p.QUIT:
                    session = False
                    if multiplayer:
                        if pt == 1:
                            state = game.resign(playerColor = True)
                        elif pt == 2:
                            state = game.resign(playerColor = False)
                    elif secondplayer:
                        state = game.resign(game.get_turn())
                    else:
                        state = game.resign(player)
                    p.quit()
                    sys.exit()
                elif event.type == p.MOUSEBUTTONDOWN and _IN_GAME:
                    if event.button == 1 or event.button == 3:  # limits it to left and right mousebuttons
                        location = p.mouse.get_pos()
                        col,row = location
                        col = col // _SQLEN
                        row = row // _SQLEN

                        if row > 8 or col > 8:
                           if quit_button.collidepoint((location[0],location[1])):
                                print("Leaving game early at turn:",game._turnNum)
                                session = False
                                if multiplayer:
                                    if pt == 1:
                                        state = game.resign(playerColor = True)
                                    elif pt == 2:
                                        state = game.resign(playerColor = False)
                                    res = client.send(game.board_to_string())
                                    print("res is: ", res)
                                    if res and res != game.board_to_string():
                                        game.string_to_board(res)
                                elif secondplayer:
                                    state = game.resign(game.get_turn())
                                else:
                                    state = game.resign(player)
                                MainMenu(p.display.set_mode((_WIDTH, _HEIGHT)),clock)

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

#                        if ty < 8:		# Only checks clicks that are on gameboard
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
                            if multiplayer:
                                if pt == 1 and game.get_turn():
                                    state = movePiece(game, moveClicks)
                                elif pt == 2 and not game.get_turn():
                                    state = movePiece(game, moveClicks)
                            else:
                                state = movePiece(game, moveClicks)
                            if state == "PROMOTION":
                                promote = moveClicks[1]
                            selectedSquare = ()
                            moveClicks.clear()
                            validMoves.clear()
          if state == "PROMOTION":
                state = promotePawn(screen, game, promote)
                promote = ()
          if _IN_GAME:
            if multiplayer:
                res = client.send(game.board_to_string())
                print("res is: ", res)
                if res and res != game.board_to_string():
                    game.string_to_board(res)
                print("TURN IS ", game._turn)
            drawChessGame(screen, game, moveClicks, validMoves)
            quit_button = InGameMenu(screen, clock, game.get_turn())
            if state == "STALEMATE" or state == "BLACK_CHECKMATED" or state == "WHITE_CHECKMATED":
                drawChessEndgame(screen, clock, game, state, 2)
            # p.display.set_mode((_WIDTH-256, _HEIGHT))
    #        elif _ON_MENU:
    #            IngameMenu(screen, clock)
          clock.tick(_MINFPS)
          p.display.flip()    # updates the screen


# MENU UTILITIES ---------------------------------------------------------------

def drawButton(screen, color, ren, button):
    draw = p.draw.rect(screen, color, button)   # creates rect object
    loc = ren.get_rect(center = draw.center)    # gets the center
    screen.blit(ren, loc)   # displays the text over button center


# MENUS ------------------------------------------------------------------------

def InGameMenu(screen, clock, turn):
    """ ()-> None
    this function draws the in-game menu system to interact with
    """
    info = p.Surface((384,384))
    info.fill(p.Color(240,234,214))
    menu = p.Surface((384,128))
    menu.fill("gray30")
    screen.blit(info,(512,0))
    screen.blit(menu,(512,384))

    count = 416

    turn_button = p.Rect(_SQLEN * 8, 0, _SQLEN * 6, 30)
    quit_button = p.Rect(_SQLEN * 8 + 100, count, _SQLEN * 3 - 10, 50)

    turnText = "White" if turn else "Black"
    turnFill = "black" if turn else "white"

    font = p.font.SysFont('Arial', 25)
    quit = font.render("Quit", True, p.Color("white"))
    turn = font.render(turnText + " Turn", True, p.Color(turnText.lower()))

    drawButton(screen, "red", quit, quit_button)
    drawButton(screen, turnFill, turn, turn_button)

    return quit_button


def PlayerOptionMenu(screen, clock, mode: bool = False):
    """ ()-> None
    this function draws to the screen the option menu when the
    singleplayer and multiplayer buttons are clicked. Singleplayer
    shows up the color picker for the players, while multiplayer
    displays local and online button prompts.
    """
    # mode decides whether to show local/multiplayer options
    # or color picker ones
    choice_label = p.Rect(_SQLEN, 150, _SQLEN * 6, 50)
    option1_button = p.Rect(_SQLEN * 2, 205, _SQLEN * 4, 50)
    option2_button = p.Rect(_SQLEN * 2, 260, _SQLEN * 4, 50)
    back_button = p.Rect(_SQLEN * 2, 315, _SQLEN * 4, 50)

    font = p.font.SysFont('Arial', 25)

    if mode:
        choice_text = "Two-player Local Device or Online"
        option1_text = "Local"
        option2_text = "Online"
    else:
        choice_text = "Choose color to control"
        option1_text = "White"
        option2_text = "Black"
    choice = font.render(choice_text, True, p.Color("white"))
    option1 = font.render(option1_text, True, p.Color("white"))
    option2 = font.render(option2_text, True, p.Color("white"))
    back = font.render("Main Menu", True, p.Color("white"))

    screen.blit(_IMAGES['mainmenu_bg'], (0,0))

    session = True

    while session:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = p.mouse.get_pos()
                    if option1_button.collidepoint((x,y)):
                        if mode:
                            session = False
                            Chess.delete_saves()
                            print("Starting local session")
                            ChessGame(p.display.set_mode((_FULLWIDTH, _HEIGHT)),clock,turn = None,load = False)
                        else:
                            session = False
                            print("Player is White")
                            Chess.delete_saves()
                            ChessGame(p.display.set_mode((_FULLWIDTH, _HEIGHT)),clock,turn = None,aimode = True,load = False,player = True)
                    if option2_button.collidepoint((x,y)):
                        if mode:
                            session = False
                            print("Starting Online...")
                            ChessGame(p.display.set_mode((_FULLWIDTH, _HEIGHT)),clock,turn = None,load = False, multiplayer=True)
                        else:
                            session = False
                            print("Player is Black")
                            ChessGame(p.display.set_mode((_FULLWIDTH, _HEIGHT)),clock,turn = None,aimode = True,load = False,player = False)
                    if back_button.collidepoint((x,y)):
                            session = False
                            print("Back to Main Menu")
                            MainMenu(screen,clock)

        drawButton(screen, "black", choice, choice_label)
        drawButton(screen, "gray30", option1, option1_button)
        drawButton(screen, "gray30", option2, option2_button)
        drawButton(screen, "gray30", back, back_button)

        clock.tick(_MINFPS)
        p.display.update()


def LoadSaveMenu(screen, clock):
    input_label = p.Rect(_SQLEN, 150, _SQLEN * 6, 50)
    back_button = p.Rect(_SQLEN * 2, 205, _SQLEN * 4, 50)

    font = p.font.SysFont('Arial', 25)
    back = font.render("Main Menu", True, p.Color("white"))
    input_text = font.render("Click on this to enter turn number", True, p.Color("white"))

    session = True
    active = False
    text = ""

    screen.blit(_IMAGES['mainmenu_bg'], (0,0))

    while session:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
            if event.type == p.MOUSEBUTTONDOWN:
                # If the user clicked on the input box rect.
                if input_label.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                    text = "|"  # render the text prompt cursor
                    input_text = font.render(text, True, p.Color("white"))
                    text = text[:-1]
                else:
                    active = False

                # if the user clicked on the main menu button
                if back_button.collidepoint(event.pos):
                    print("Main Menu")
                    session = False
                    print("Back to Main Menu")
                    MainMenu(screen,clock)

            if event.type == p.KEYDOWN:
                if active:
                    if event.key == p.K_RETURN or event.key == p.K_KP_ENTER:
                        if text:
                          try:
                            inturn = int(text)
                            session = False
                            ChessGame(p.display.set_mode((_FULLWIDTH, _HEIGHT)),clock, turn = inturn, load = True)
                          except ValueError:
                            text = ""   # user put in non integer, clear input
                    elif event.key == p.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                    text += "|" # render text prompt cursor
                    input_text = font.render(text, True, p.Color("white"))
                    text = text[:-1]

        # draw the buttons
        drawButton(screen, "black", input_text, input_label)
        drawButton(screen, "gray30", back, back_button)

        # update the full display
        p.display.flip()


# this will be opened first, and it's what will call the game to run.
def MainMenu(screen, clock):
    loadMenuImages()        # load the relevant images
    p.display.set_caption("Chess")  # caption the title as "Chess"
    p.display.set_icon(_IMAGES['icon']) # set the icon

    # create the Rect with a different top value based on the count
    count = 100
    play_button = p.Rect(_SQLEN * 2, count, _SQLEN * 4, 50)
    count += 100
    multi_button = p.Rect(_SQLEN * 2, 200, _SQLEN * 4, 50)
    count += 100
    load_button = p.Rect(_SQLEN * 2, count, _SQLEN * 4, 50)
    count += 100
    quit_button = p.Rect(_SQLEN * 2, count, _SQLEN * 4, 50)

    # prepare the text for the buttons
    font = p.font.SysFont('Arial', 25)
    play = font.render("Single Player", True, p.Color("white"))
    multi = font.render("Multiplayer", True, p.Color("white"))
    load = font.render("Load Previous", True, p.Color("white"))
    quit = font.render("Quit", True, p.Color("white"))

    # set the default button color
    button_color = p.Color("gray30")
    session = True

    # load the background image
    screen.blit(_IMAGES['mainmenu_bg'], (0,0))

    # menu loop
    while session:
        for event in p.event.get():
            if event.type == p.QUIT:
                # if they press the x in the corner, forcibly quit
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = p.mouse.get_pos()

                    # open the option menu with color focus
                    if play_button.collidepoint((x,y)):
                        print("Selecting color to control")
                        session = False
                        PlayerOptionMenu(screen,clock)

                    # open the option menu with local/online focus
                    if multi_button.collidepoint((x,y)):
                        print("Selecting Multiplayer options")
                        session = False
                        PlayerOptionMenu(screen,clock,mode = True)

                    # open the loadsavemenu
                    if load_button.collidepoint((x,y)):
                        print("Loading Previous Session")
                        session = False
                        LoadSaveMenu(screen, clock)

                    # quit the program if quit button is clicked
                    if quit_button.collidepoint((x,y)):
                        print("Quitting...")
                        session = False
                        p.quit()
                        sys.exit()

        # draw the main menu buttons
        drawButton(screen, button_color, play, play_button)
        drawButton(screen, button_color, multi, multi_button)
        drawButton(screen, button_color, load, load_button)
        drawButton(screen, "red", quit, quit_button)

        clock.tick(_MINFPS)
        p.display.update()

if __name__ == "__main__":
    p.init()        # initialize pygame
    clock = p.time.Clock()
    screen = p.display.set_mode((_WIDTH, _HEIGHT))
    #ChessGame(screen, clock) # main game for the board
    MainMenu(screen,clock)
    # will likely want to return to main menu of the whole game system
