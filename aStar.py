import math

#aStar conceptual understanding from 
#https://www.youtube.com/watch?v=-L-WgKMFuhE
#Note: Did NOT copy pseudocode. Just used for conceptual understanding

#Node class is helpful for the searching part
#All it does is associate a cell with its pathfinding info
#like it's parent node and costs 
class Node:
    def __init__(self, row, col, parent = None):
        self.parent = parent
        self.row = row
        self.col = col
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return (self.col == other.col) and (self.row == other.row)

    def __repr__(self):
        return f"Node({self.row}, {self.col}, {self.g}, {self.h}, {self.f} {self.parent})"

def findCell(x, y, rows, cols, cellWidth, cellHeight):
    #if it's on screen
    if 0 < (x // cellWidth) < cols:
        if 0 < (y // cellHeight) < rows:
            #row, col
            return (int(y // cellHeight), int(x // cellWidth))

def convertToBoard(app):
    #convert the current state of the app to a 2D array
    #for now, 11 x 11 because was goign to do 10 x 10 but odd is better to 
    #clearly define destination (player)
    board = [([0] * app.boardCols) for row in range(app.boardRows)]
    cellWidth = app.width/app.boardRows
    cellHeight = app.height/app.boardCols
    #make player grid empty always, so that the alien knows it can go into it, 
    #to find the player
    board[5][5] = 0
    #now, we have a board where empty cells are marked with a 0. So we can perform A* 
    #on this board with the player cell as the goal, avoiding cells with a value of 1
    return board

def findPath(startNode):
    tracedPath = []
    while startNode:
        tracedPath.append((startNode.row, startNode.col))
        startNode = startNode.parent
    #reversed because we want it to go from first move to last move
    return tracedPath[::-1]

def legalMove(row, col, rows, cols, board):
    if (0 <= row < rows) and (0 <= col < cols) and (board[row][col] != 1):
        return True
    return False

def getFCost(node):
    return node.f

def getEuclideanDistance(nodeA, nodeB):
    return math.sqrt((nodeA.row - nodeB.row)**2 + (nodeA.col - nodeB.col)**2)
    
def aStar(board, destination, alienCoords):
    #alienRow, alienCol = findCell(alienX, alienY, 11, 11, app.width/11, app.height/11)
    #alienNode = Node(alienRow, alienCol)
    alienNode = Node(alienCoords[0], alienCoords[1])
    destinationNode = Node(destination[0], destination[1])
    #the first element in notExplored is always the one with the least cost
    notExplored = []
    #this can be a set since we don't need it to be ordered
    #and we use the in operator on it
    explored = set()
    notExplored.append(alienNode)
    while notExplored != []:
        #key argument allows us to sort notExplored by each elements output
        #of the function we pass in as the "key"
        notExplored = sorted(notExplored, key = getFCost)
        currentNode = notExplored.pop(0)
        explored.add((currentNode.row, currentNode.col))
        if currentNode == destinationNode:
            result = findPath(currentNode)
            return result
        #the neighboring nodes are simply the nodes in all 4 directions
        #the aliens can't move diagonally since that would mean one of 
        #their moves covers more distance than another
        #the list is just tuples of rows and cols to make the legality check easier
        borderingNodes = [(currentNode.row, currentNode.col + 1),
                            (currentNode.row, currentNode.col - 1),
                            (currentNode.row + 1, currentNode.col), 
                            (currentNode.row - 1, currentNode.col)]
        for border in borderingNodes:
            if legalMove(border[0], border[1], len(board), len(board[0]), board) and (border not in explored):
                borderingNode = Node(border[0], border[1], parent = currentNode)
                #distance from starting node will just be 1 greater than parent
                borderingNode.g = currentNode.g + 1
                borderingNode.h = getEuclideanDistance(borderingNode, destinationNode)
                borderingNode.f = borderingNode.g + borderingNode.h
                if borderingNode not in notExplored:
                    #add this neighbor to be explored later
                    notExplored.append(borderingNode)


board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]]

alienCoords = (4, 0)
goal = (5, 5)

path = aStar(board, goal, alienCoords)
print(path)
