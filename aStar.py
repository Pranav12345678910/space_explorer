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
            return (x // cellWidth, y // cellHeight)


def convertToBoard(app):
    #convert the current state of the app to a 2D array
    #for now, 11 x 11 because was goign to do 10 x 10 but odd is better to 
    #clearly define destination (player)
    rows = 11
    cols = 11
    board = [([0] * cols) for row in range(rows)]
    cellWidth = app.width/rows
    cellHeight = app.height/cols
    #if the cell is occupied, put 1 in it
    for x in app.dots:
        pendingCell = findCell(x.x, x.y, rows, cols, cellWidth, cellHeight)
        if pendingCell != None:
            row, col = pendingCell
            board[int(row)][int(col)] = 1
    #make player grid empty always, so that the alien knows it can go into it, 
    #to find the player
    board[5][5] = 0
    goal = (5, 5)
    #now, we have a board where empty cells are marked with a 0. So we can perform A* 
    #on this board with the center cell as the goal, avoiding cells with a value of 1
    return (board, goal)

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
    
def aStar(board, goal, alienCoords):
    #make cellWidth and cellHeight app attributes later
    #and rows and cols
    #alienRow, alienCol = findCell(alienX, alienY, 11, 11, app.width/11, app.height/11)
    #alienNode = Node(alienRow, alienCol)
    alienNode = Node(*alienCoords)
    goalNode = Node(*goal)
    #the first element in notExplored is always the one with the least cost
    notExplored = []
    #this can be a set since we don't need it to be ordered
    #and we use the in operator on it
    explored = set()
    notExplored.append(alienNode)
    while notExplored:
        notExplored = sorted(notExplored, key = getFCost)
        currentNode = notExplored.pop(0)
        if currentNode == goalNode:
            return findPath(currentNode)
        explored.add((currentNode.row, currentNode.col))
        #the neighboring nodes are simply the nodes in all 4 directions
        #the aliens can't move diagonally since that would mean one of 
        #their moves covers more distance than another
        #the list is just tuples of rows and cols to make the legality check easier
        neighboringNodes = [(currentNode.row + 1, currentNode.col), 
                            (currentNode.row - 1, currentNode.col), 
                            (currentNode.row, currentNode.col + 1),
                            (currentNode.row, currentNode.col - 1)]
        for neighbor in neighboringNodes:
            if legalMove(*neighbor, len(board), len(board[0]), board) and neighbor not in explored:
                neighboringNode = Node(*neighbor, parent = currentNode)
                #distance from starting node will just be 1 greater than parent
                neighboringNode.g = currentNode.g + 1
                neighboringNode.h = getEuclideanDistance(neighboringNode, goalNode)
                neighboringNode.f = neighboringNode.g + neighboringNode.h
                if neighboringNode not in notExplored:
                    #add this neighbor to be explored later
                    notExplored.append(neighboringNode)

board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]]

alienCoords = (4, 0)
goal = (5, 5)

path = aStar(board, goal, alienCoords)
print(path)