from MancalaClass import Mancala, getListOfLegalMoves, returnBoard
class Node(object):
    def __init__(self, data, prevMove, adjFactor):
        self.data = data
        self.children = []
        self.prevMove = prevMove
        self.turn = "x"
        self.bestMove = "x"
        self.value = (sum(self.data[1][:6]) + (adjFactor * self.data[1][6])) - (sum(self.data[1][7:13]) + (adjFactor * self.data[1][13]))

    def add_child(self, obj):
        self.children.append(obj)

def makeChildren(node, max, count, adjFactor):
    for move in node.data[2]:
        temp = Node(returnBoard(node.data[1], move, node.data[0]), move, adjFactor)
        temp.turn = temp.data[0]
        node.add_child(temp)
    if count < max-2:
        for c in node.children:
            makeChildren(c, max, count+1, adjFactor)


def minimax(position, depth, maximizingPlayer):
    #if game is over
    if sum(position.data[1][:6]) == 0 or sum(position.data[1][7:13]) == 0 or position.data[1][6] > 24 or position.data[1][13] > 24:
        if sum(position.data[1][:7]) > sum(position.data[1][7:]) or position.data[1][6] > 24:
            return 500
        elif sum(position.data[1][:7]) < sum(position.data[1][7:]) or position.data[1][13] > 24:
            return -500
        else:
            return 0
    if depth == 0:
        #print((sum(position.data[1][:6]) + 2*position.data[1][7]) - (sum(position.data[1][7:13]) + 2*position.data[1][13]))
        return (position.value)
    if maximizingPlayer == 1:
        maxEval = -500
        for c in position.children:
            eval = minimax(c, depth-1, c.turn)
            if maxEval < eval:
                maxEval = eval
                position.bestMove = c.prevMove
        return maxEval
    elif maximizingPlayer == 2:
        minEval = 500
        for c in position.children:
            eval = minimax(c, depth-1, c.turn)
            if minEval > eval:
                minEval = eval
                position.bestMove = c.prevMove
        return minEval
    else:
        print("oops")


def printMoves(node):
    for c in node.children:
        if c.prevMove == node.bestMove:
            print(c.prevMove)
            printMoves(c)
#has to be one less than number of layers
def findBestMove(board, turn, numberOfNodes, adjFactor):
    node = Node([turn, board, getListOfLegalMoves(board, turn)], 'x', adjFactor)
    node.turn = turn
    makeChildren(node, numberOfNodes, 0, adjFactor)
    print("worst score:",minimax(node, numberOfNodes-1,node.turn))
    printMoves(node)
    return node.bestMove
