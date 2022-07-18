"""
Driver File
Responsablities:
1. user input
2. game state
"""
import pygame as p
import ChessEngine



#Image quality
WIDTH = HEIGH = 512 #400 is another option
DIMENSION = 8 #dimension of board
SQ_SIZE = HEIGH // DIMENSION
MAX_FPS = 15 #animation
IMAGES = {}

"""
We want to load images only once
Load images will initialize a global dict of images
Only run exactly once
"""

def loadImages():
    pieces = ['wp', 'bp', "bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK"]
    for i in pieces:
        IMAGES[i] = p.transform.scale(p.image.load(f"images\\{i}.png"), (SQ_SIZE, SQ_SIZE))


"""
MAIN DRIVER
handle user input
handle graphics
"""

def main():
    #Startup pygame
    p.init()

    #Setting up the game
    screen = p.display.set_mode((WIDTH, HEIGH))
    clock = p.time.Clock()
    screen.fill(p.Color(1,1,181))
    gs = ChessEngine.GameState()

    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for a move

    running = True
    sqSel = () #keep track of last click, tuple(row,col)
    playerClicks = [] #keep track of player clicks, 2 tuples[(Row,Col),(Row,Col)]
    #Loading images
    loadImages() #do only once

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #Mouse event handles
            elif e.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos() #get x,y 
                col = loc[0]//SQ_SIZE
                row = loc[1]//SQ_SIZE
                if sqSel == (row, col): #user clicked same square twice
                    sqSel = ()
                    playerClicks = []
                
                else:
                    sqSel = (row, col)
                    playerClicks.append(sqSel)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)   
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSel = () #reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSel]
                    
            #key handle
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when z is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    '''
    Responsible for graphic in game state
    '''
    drawBoard(screen)               #draw squares on board
    #add piece highlighting or move suggestion
    drawPieces(screen, gs.board)    #draw the pieces on board


def drawBoard(screen):
    colors = [p.Color("white"), p.Color(1,1,181)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": 
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()

