from objects.chess.chess import Chess
import pygame as p
import sys

# knowing the width and height (pixel count/area of screen)
# dimensions of board is usually always 8
# need to know the length of the squares and something global to hold the images
# and probably a set FPS for drawing

_WIDTH = _HEIGHT = 516
_DIMENSIONS = 8
_SQLEN = _HEIGHT // _DIMENSIONS
_IMAGES = {}    # dictionary/hashmap. For quick image lookup
_MINFPS = 15
_MAXFPS = 30

# need to load the images
def loadImages():
    pieces = [
        'bbishop', 'bking', 'bknight', 'bpawn', 'bqueen', 'brook',
        'wbishop', 'wking', 'wknight', 'wpawn', 'wqueen', 'wrook'
    ]
    for piece in pieces:
        _IMAGES[piece] = p.transform.scale(p.image.load("resources/chess/" + piece + ".png"), (_SQLEN, _SQLEN))

# need to draw the game
def drawGame(screen, game):
    drawScreen(screen)
    drawPieces(screen, game.get_board())

def drawScreen(screen):
    colors = [p.Color("white"), p.Color("gray")]
    drawWhite = True
    for r in range(_DIMENSIONS):
        for c in range(_DIMENSIONS):
            if drawWhite:
                p.draw.rect(screen, colors[0], [_SQLEN*c, _SQLEN*r, _SQLEN, _SQLEN])
                drawWhite = False
            else:
                p.draw.rect(screen, colors[1], [_SQLEN*c, _SQLEN*r, _SQLEN, _SQLEN])
                drawWhite = True
        if r % 2 == 0:
            drawWhite = False
        else:
            drawWhite = True

def drawPieces(screen, board):
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

def main_menu(screen, clock):
    while True:
        screen.fill((0,0,0))
        draw_text('')

# need some type of main function that runs in a loop with an exit condition
# pygame has an event logger and can interface with the exit button
def ChessGame(screen, clock):
    screen.fill(p.Color("white"))
    loadImages()
    p.display.set_caption("Chess")
    p.display.set_icon(_IMAGES['brook'])
    game = Chess()  # need to initialize the game by calling the class
    session = True

    # game loop
    while session:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    session = False
        drawGame(screen, game)
        clock.tick(_MINFPS)
        p.display.flip()    # updates the screen

if __name__ == "__main__":
    p.init()        # initialize pygame
    clock = p.time.Clock()
    screen = p.display.set_mode((_WIDTH, _HEIGHT))
    ChessGame(screen, clock) # main game for the board
    # will likely want to return to main menu of the whole game system
