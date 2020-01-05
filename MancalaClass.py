import copy
class Mancala:
    def __init__(self, board = [4,4,4,4,4,4,0,4,4,4,4,4,4,0]):
        self.board = board
        self.houses = [{1:6, 2:13},{6:1, 13:2}]
        self.turn = 1
    #method for checking if a player is on their side or their opponents
    def checkLegalSide(self, choice):
        if self.turn == 1:
            return (0 <= choice <= 5)
        elif self.turn == 2:
            return (7 <= choice <= 12)
        else:
            return False
    #method for moving the pieces. Represents 1 turn
    def move(self, position):
        if self.checkLegalSide(position) and self.board[position] != 0:
            hand = self.board[position]
            self.board[position] = 0

            for i in range(1,hand+1):
                #skips hole if it is opponent's house
                if self.houses[1].get(position+1) == self.oppositeTurn():
                    position += 1

                #adds to the position
                position += 1

                # makes the board circular
                if position > 13:
                    position = 0

                self.board[position] += 1
            #checks if it landed on empty
            if self.board[position] == 1 and position != 13 and position != 6:
                self.steal(position)
            #checks whose turn it is
            if self.turn != self.houses[1].get(position):
                self.changeTurns()
            self.checkOver()
        else:
            print("illegal move")
    def steal(self, position):
        if self.checkLegalSide(position) and self.board[12-position] != 0:
            total = self.board[position] + self.board[12-position]
            self.board[position] = 0
            self.board[12 - position] = 0
            #add to house
            self.board[self.houses[0].get(self.turn)] += total
    #changes turns
    def changeTurns(self):
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
    #returns opposite turn
    def oppositeTurn(self):
        if self.turn == 1:
            return 2
        elif self.turn == 2:
            return 1
    #returns 0 if game is over, 1 is game is still going
    def checkOver(self):
        # if any holes still have something
        if sum(self.board[:6]) == 0 or sum(self.board[7:13]) == 0:
            return self.checkWhoWon()

    def checkWhoWon(self):
        self.board[6] = sum(self.board[:7])
        self.board[13] =  sum(self.board[7:])

        for i in range(len(self.board)-1):
            if i != 6:
                self.board[i] = 0

        if self.board[6] > self.board[13]:
            print("Blue wins")
            return 1
        elif self.board[6] < self.board[13]:
            print("Red wins")
            return 2
        else:
            print("tie")
            return 3

def getListOfLegalMoves(board, turn):
    listOfLegalMoves = []
    game = Mancala()
    game.board = board
    game.turn = turn
    for i, hole in enumerate(board):
        if game.checkLegalSide(i) and hole != 0:
            listOfLegalMoves.append(i)
    return listOfLegalMoves
#
def returnBoard(board, move, turn):
    mancalaGame = Mancala()
    mancalaGame.board = board
    mancalaGame.turn = turn
    temp = copy.deepcopy(mancalaGame)
    temp.move(move)
    if temp.turn == mancalaGame.turn:
        return [mancalaGame.turn, temp.board, getListOfLegalMoves(temp.board, mancalaGame.turn)]
    else:
        return [mancalaGame.oppositeTurn(), temp.board, getListOfLegalMoves(temp.board, mancalaGame.oppositeTurn())]
