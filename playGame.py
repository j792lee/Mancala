BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,204)
counter = 0
board = [4,4,4,4,4,4,0,4,4,4,4,4,4,0]
from MancalaClass import Mancala
import sys
import pygame
import tree

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 50)
winfont = pygame.font.SysFont('Comic Sans MS', 125)

COLUMNCOUNT = 2
ROWCOUNT = 6
circleCoordinates = []

RADIUS = int(52)
width = 412
height = 960

game = Mancala(board)

size = (width, height)
screen = pygame.display.set_mode(size)
bg = pygame.image.load("mancala.png").convert()
textsurface = []
for i in game.board:
    textsurface.append(myfont.render(str(i), False, (0, 0, 0)))

winsurface = []
winsurface.append(winfont.render("Blue wins", False, BLUE))
winsurface.append(winfont.render("Red wins", False, RED))


#adds the coordinates of the centre of all circles to a list. Returns that list
def makeLisOfCircleCoordinates(circleCoordinates):
    for c in range(COLUMNCOUNT):
        for r in range(ROWCOUNT):
            circleCoordinates.append([int(200*c+103), int(199 + 112*r)])
    return circleCoordinates
#reindx list to fit mancala class
def reindexList(circleList):
    newList = []
    for i in range(len(circleList)+2):
        if i <= 5:
            newList.append(circleList[i])
        elif i == 6:
            newList.append([208, 882])
        elif 6 < i < 13:
            newList.append(circleList[len(circleList)-(i-6)])
        else:
            newList.append([208, 84])
    return newList

def checkIfInCircle(coordinates):
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]

    sqx = (x - coordinates[0]) ** 2
    sqy = (y - coordinates[1]) ** 2

    if (sqx + sqy) ** 0.5 < RADIUS:
        return True
    return False

def highlight(coordinates, colour, radius):
    pygame.draw.circle(screen, colour, coordinates, radius, 5)

circleCoordinates = makeLisOfCircleCoordinates(circleCoordinates)
circleCoordinates = reindexList(circleCoordinates)

if board == [4,4,4,4,4,4,0,4,4,4,4,4,4,0]:
    bestMove = 5
else:
    bestMove = tree.findBestMove(board,1,6,1.2)
while True:
    for event in pygame.event.get():

        pygame.display.flip()
        screen.blit(bg, [0, 0])
        #quit event
        if event.type == pygame.QUIT:
            sys.exit()
            # prints win text
        if game.checkOver():
            screen.blit(winsurface[game.checkOver() - 1], (0, 0))
        else:
            #Turn shower
            if game.turn == 1:
                for circleNum, circle in enumerate(circleCoordinates):
                    if circleNum < 6:
                        highlight(circle, BLUE, RADIUS + 5)
            else:
                for circleNum, circle in enumerate(circleCoordinates):
                    if 13 > circleNum > 6:
                        highlight(circle, RED, RADIUS + 5)

        # circle clicks and highlight
        for circleNum, circle in enumerate(circleCoordinates):
            if bestMove == circleNum:
                highlight(circle, YELLOW, RADIUS+5)
            if checkIfInCircle(circle) and circleNum != 6 and circleNum != 13:
                highlight(circle, BLACK, RADIUS)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    counter += 1
                    game.move(circleNum)
                    if counter < 5:
                        print("level 1")
                        bestMove = tree.findBestMove(game.board, game.turn, 6, 2)
                    elif 5 <= counter <= 15:
                        print("level 2")
                        bestMove = tree.findBestMove(game.board, game.turn, 6, 1.5)
                    else:
                        print("level 3")
                        bestMove = tree.findBestMove(game.board, game.turn, 7, 1)
                    print(bestMove)
        # Adds all the number of beads in each hole to a list for printing
        for i in range(len(game.board)):
            textsurface[i] = myfont.render(str(game.board[i]), False, (0, 0, 0))
        # prints each hole's value
        for i in range(len(circleCoordinates)):
            screen.blit(textsurface[i], circleCoordinates[i])







