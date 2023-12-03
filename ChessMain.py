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
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'bQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("/images/" + piece + '.png'), (SQ_SIZE, SQ_SIZE))

# main driver for code: will handle input and updating the graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            clock.tick(MAX_FPS)
            p.display.flip()

if __name__ == "__main__":
    main()