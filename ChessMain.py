# Main driver file. Will be responsible for handling user inpput and displaying current GameState object

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

# Initialize a global dictionary of images
def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + '.png'), (SQ_SIZE, SQ_SIZE))
        # this accesses the directory with images and maps an image to a piece

# main driver for code: will handle input and updating the graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    # showMoves = True
    moveMade = False
    loadImages()

    running = True
    sqSelected = () #keep track of last square selected. (x, y)
    playerClicks = [] #keep track of player clicks. Two tuples.
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            
            #mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of mouse
                col = location[0]//SQ_SIZE; row = location[1]//SQ_SIZE
                sqSelected = (row, col)
                piece = gs.board[row][col]
                if len(playerClicks)!=0 and playerClicks[0] == (row, col): #the user clicked the same square twice
                    sqSelected = () #deselect
                    playerClicks = []
                elif len(playerClicks) == 1:
                    if (not gs.white_to_move and piece[0] != 'b') or (gs.white_to_move and piece[0] != 'w'):
                        playerClicks.append(sqSelected)
                elif (gs.white_to_move and piece[0] == 'w') or (not gs.white_to_move and piece[0] == 'b'):
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True 
                    sqSelected = (); playerClicks = [] #reset selected move/square
                elif len(playerClicks) == 1: #and showMoves:
                    validMoves = gs.getValidMoves(playerClicks[0][0], playerClicks[0][1])
                    for m in validMoves:
                        p.draw.rect(screen, p.Color("blue"), p.Rect(SQ_SIZE*m.endCol, SQ_SIZE *m.endRow, SQ_SIZE, SQ_SIZE), 4)

            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove() # undo move when 'z' is pressed
                    moveMade = True
                if e.key == p.K_m:
                    showMoves = not showMoves

        if len(playerClicks) != 1:
            validMoves = gs.getValidMoves()

        if len(playerClicks) != 1:
            drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

# responsible for all the graphics within a current game
def drawGameState(screen, gs):
    drawBoard(screen) # draw squares on the board
    drawPieces(screen, gs.board) # draw pics on top of squares


# draw the squares on the board
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            # if the addition of r and c mod 2 has a remainder of 0, the square should be colored light
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# draw the pieces on the board using the current GameState.board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
    main()