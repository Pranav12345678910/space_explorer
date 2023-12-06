from cmu_graphics import *
from PIL import Image
import copy
import random
from planet import Planet
import math
from solarSystem import solarSystem
from materials import Material
from player import Player
from tool import Tool
from armour import Armour
import aStar
from alien import Alien
import voronoi

#To do:
#fix stamina bug
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#colors
darkGreen = rgb(0, 102, 0)
lightGreen = rgb(51, 204, 51)
darkBrown = rgb(102, 51, 0)
lightBrown = rgb(153, 102, 51)
middleGreen = rgb(0, 153, 51)
sand = rgb(194, 178, 128)
gray = rgb(191, 202, 219)

def loadAssets(app):
    #images (for materials and sprites)
    #cmu_graphics image knowledge from Pat Virtue's lecture slides:
    #https://www.cs.cmu.edu/~112/lecture/15112_F23_Lec2_Week12_OOP2_inked.pdf
    #citation: https://www.flaticon.com/free-icon/wood_3275748
    app.woodImage = CMUImage(Image.open("images\\3275748.png"))
    #citation: https://www.flaticon.com/free-icon/metal_5672236
    app.metalImage = CMUImage(Image.open("images\\5672236.png"))
    #citation: https://www.freepik.com/icon/astronaut_360850#fromView=resource_detail&position=6
    app.playerImage = CMUImage(Image.open("images\\astronaut-icon-274x512-oyvau7j5.png"))
    #citation: https://iconduck.com/icons/169421/alien
    app.weakAlienImage = CMUImage(Image.open("images\\alien.png"))
    #citation: https://www.flaticon.com/free-icon/alien_6542680
    app.strongAlienImage = CMUImage(Image.open("images\\strongAlien.png"))
    #materials 
    app.wood = Material(10, 30, "wood", 10, app.woodImage)
    app.metal = Material(10, 30, "metal", 10, app.metalImage)
    #tools
    app.axe = Tool(3, {app.wood: 10, app.metal: 1}, 1, "axe", 100, {app.wood: 5, app.metal: 3})
    app.pickaxe = Tool(2, {app.metal: 10, app.wood: 1}, 1, "pickaxe", 100, {app.wood: 5, app.metal: 3})
    app.sword = Tool(4, {app.wood: 1, app.metal: 1}, 3, "sword", 100, {app.wood: 2, app.metal: 4})
    app.hand = Tool(1, {app.wood: 1, app.metal: 1}, 1, "hand", 100, {})
    app.toolList = [app.axe, app.pickaxe, app.sword, app.hand]
    #armours
    app.skin = Armour(1, 1, "skin")
    app.chainmail = Armour(3, 0.5, "chainmail")
    #aliens
    app.weakAlien = Alien(app.hand, app.skin, app.weakAlienImage, 50)
    app.strongAlien = Alien(app.sword, app.chainmail, app.strongAlienImage, 50)

def newGame(app):
    loadAssets(app)
    loadMisc(app)
    loadPlayer(app)
    loadPlanetSolarSystem(app)
    loadButtonInfo(app)

def loadPlayer(app):
    app.player = Player()
    app.player.currTool = app.hand
    app.player.currArmor = app.skin

def loadPlanetSolarSystem(app):
    #top left, width, height
    app.planetDotGenerationWindow = [app.width/2 - 3 * app.width/2, 
                                     app.height/2 - 3 * app.height/2, 
                                     3 * app.width, 3 * app.height]
    app.voronoiSeeds = voronoi.getSeeds((app.planetDotGenerationWindow[0], 
                                        app.planetDotGenerationWindow[0] + 
                                        app.planetDotGenerationWindow[2]), 
                                        (app.planetDotGenerationWindow[1], 
                                         app.planetDotGenerationWindow[1] +
                                        app.planetDotGenerationWindow[3]), 
                                        app.numSeeds)
    app.planets = [Planet("green", 270, app.planetDotGenerationWindow[2], 
                          app.planetDotGenerationWindow[3], app.width, 
                          app.height, (app.wood, app.metal), 10, (app.weakAlien,), 
                          app.voronoiSeeds), 
                          Planet("blue", 270, app.planetDotGenerationWindow[2], 
                                 app.planetDotGenerationWindow[3], 
                                 app.width, app.height, (app.wood, app.metal), 10, 
                                 (app.weakAlien,), 
                                 app.voronoiSeeds), 
                                 Planet("purple", 270,
                                        app.planetDotGenerationWindow[2], 
                                        app.planetDotGenerationWindow[3], 
                                        app.width, app.height, 
                                        (app.wood, app.metal), 10, 
                                        (app.weakAlien,), app.voronoiSeeds)]
    app.solarSystem = solarSystem(app.planets, app.width/2, app.height/2) 
    app.planet = None
    app.dots = None
    app.rotateSpeeds = [random.uniform(0, 0.5) for x in range(len(app.solarSystem.planets))]
    app.angles = [1 for x in range(len(app.solarSystem.planets))]
    app.selectedPlanet = None

def loadButtonInfo(app):
    app.inventoryIconCoords = (50, 850, 100, 100)
    app.inventoryXButton = (app.width/2 + 200, app.height/2 - 200, 50, 50)
    app.inventoryCraftButton = (app.width/2 - 200, app.height/2 - 75, 175, 50)
    app.inventoryEquipButton = (app.width/2 + 25, app.height/2 - 75, 175, 50)
    app.inventoryPressed = False
    app.inventoryGridTopLeft = (app.width/2 - 200, app.height/2)
    app.inventoryCols = app.player.inventoryCols
    app.inventoryRows = app.player.inventoryRows
    app.inventoryGridWidth = 400
    app.inventoryGridHeight = 200
    app.cellBorderWidth = 2
    app.equipPressed = False
    app.selectedRowCol = None
    app.craftPressed = False
    app.equipXButton = (575, 275, 50, 50)
    app.craftXButton = (1475, 275, 50, 50)
    app.equipToolButton = (500, 650, 200, 50)
    app.unequipToolButton = (500, 575, 200, 50)
    app.craftingListTopLeft = (1300, 375)
    app.craftingCellWidth = 200
    app.craftingCellHeight = 50
    app.craftedImpossible = False
    app.playerCoords = [app.width/2, app.height/2]
    app.healthLabel = (app.width/2, app.height - 200)

def loadMisc(app):
    app.usePlayerCoordsX = False
    app.usePlayerCoordsY = False
    app.playerSize = 50
    app.boardRows = 11
    app.boardCols = 11
    app.playerHit = False
    app.counter = 0
    app.stepsPerSecond = 30
    app.gameOver = False
    app.paused = False
    app.stepCounter = 0
    app.maxDotsPerVoronoiZone = 18
    app.numSeeds = 15
    app.playerMoving = False

def onAppStart(app):
    newGame(app)

def drawInventoryIcon(app):
    drawRect(*app.inventoryIconCoords, opacity = 30) 
    drawLabel("Inventory", 100, 900)   

#grid drawing conceptual understanding taken from
#tetris case study from CS Academy 
def getCellLeftTop(app, row, col): 
    cellWidth = app.inventoryGridWidth/app.inventoryCols
    cellHeight = app.inventoryGridHeight/app.inventoryRows
    cellLeft = app.inventoryGridTopLeft[0] + col * cellWidth
    cellTop = app.inventoryGridTopLeft[1]  + row * cellHeight
    return (cellLeft, cellTop)

def drawCell(app, row, col, content):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth = app.inventoryGridWidth/app.inventoryCols
    cellHeight = app.inventoryGridHeight/app.inventoryRows
    if (row, col) == app.selectedRowCol:
        drawRect(cellLeft, cellTop, cellWidth, cellHeight, border = "black", 
                 borderWidth = app.cellBorderWidth, fill = "green", opacity = 30)
    else:
        drawRect(cellLeft, cellTop, cellWidth, cellHeight, border = "black", 
                fill = "white", borderWidth = app.cellBorderWidth)
    if content == 0:
        drawLabel("empty", cellLeft + cellWidth/2, cellTop + cellWidth/2)
    else:
        drawLabel(content[0], cellLeft + cellWidth/2, cellTop + cellWidth/4)
        drawLabel(content[1].name, cellLeft + cellWidth/2, cellTop + 3 * cellWidth/4)

def drawInventoryGrid(app):
    for y in range(app.inventoryRows):
        for x in range(app.inventoryCols):
            drawCell(app, y, x, app.player.inventory[y][x])
    drawRect(app.inventoryGridTopLeft[0], app.inventoryGridTopLeft[1], 
             app.inventoryGridWidth, app.inventoryGridHeight, 
             fill = None, border = "black", 
             borderWidth = app.cellBorderWidth * 2)

def drawInventoryCloseButton(app):
    #app.inventoryXButton: (x, y, size, size)
    drawRect(app.inventoryXButton[0], app.inventoryXButton[1], 
             app.inventoryXButton[2], app.inventoryXButton[3], 
             align = "center", fill = "white", border = "black")
    drawLabel("X", app.inventoryXButton[0], app.inventoryXButton[1], size = 50)

def drawInventoryButtons(app):
    #draw crafting button
    drawRect(app.inventoryCraftButton[0], app.inventoryCraftButton[1], 
             app.inventoryCraftButton[2], app.inventoryCraftButton[3],
             fill = None, border = "black", borderWidth = app.cellBorderWidth)
    drawLabel("Craft", app.inventoryCraftButton[0] + 
              app.inventoryCraftButton[2]/2, app.inventoryCraftButton[1] + 
              app.inventoryCraftButton[3]/2)
    #draw equip button
    drawRect(app.inventoryEquipButton[0], app.inventoryEquipButton[1], 
             app.inventoryEquipButton[2], app.inventoryEquipButton[3],
             fill = None, border = "black", borderWidth = app.cellBorderWidth)
    drawLabel("Equip", app.inventoryEquipButton[0] + 
              app.inventoryEquipButton[2]/2, app.inventoryEquipButton[1] + 
              app.inventoryEquipButton[3]/2)

def drawInventory(app):
    drawRect(app.width/2, app.height/2, 500, 500, align = "center", 
             fill = "white", border = "black", 
             borderWidth = 2 * app.cellBorderWidth)
    drawLabel("Inventory", app.width/2, app.height/2 - 150, size = 100)
    drawLabel("Click on a cell to select. Click outside to empty. Press e" + 
              " to throw away only one piece", app.width/2, 100, size = 40)
    drawInventoryCloseButton(app)
    drawInventoryGrid(app)
    drawInventoryButtons(app)

def drawEquipWindow(app):
    #need to show currently equipped armor and tool
    drawRect(app.width/2 - 600, app.height/2 - 250, 300, 500, fill = "white", 
             border = "black", borderWidth = 2 * app.cellBorderWidth)
    drawLabel("Equip Armor and Tools", app.width/2 - 450, app.height/2 - 150, size = 25)
    #show equipped armor
    drawLabel(f"Currently equipped armor: {app.player.currArmor}", app.width/2 
              - 450, app.height/2 - 50, size = 20)
    #show equipped tool
    drawLabel(f"Currently equipped tool: {app.player.currTool}", app.width/2 
              - 450, app.height/2, size = 20)
    #draw close button
    drawRect(app.equipXButton[0], app.equipXButton[1], 
             app.equipXButton[2], app.equipXButton[3], 
             fill = "white", border = "black")
    drawLabel("X", app.equipXButton[0] + app.equipXButton[2]/2, 
              app.equipXButton[1] + app.equipXButton[3]/2, size = 50)
    #draw equip tool button
    drawRect(*app.equipToolButton, fill = "white", border = "black", align = "center")
    drawLabel("Equip Tool from selected Cell", app.equipToolButton[0], app.equipToolButton[1])
    #draw unequip tool button
    drawRect(*app.unequipToolButton, fill = "white", border = "black", align = "center")
    drawLabel("Unequip Current Tool", app.unequipToolButton[0], app.unequipToolButton[1])
        

def drawCraftingCells(app):
    drawRect(app.craftingListTopLeft[0], app.craftingListTopLeft[1], 
             app.craftingCellWidth, (len(app.toolList) - 1) * app.craftingCellHeight, 
             fill = None, border = "black", borderWidth = 2 * app.cellBorderWidth)
    for x in range(len(app.toolList) - 1):
        drawRect(app.craftingListTopLeft[0], app.craftingListTopLeft[1] + x * 
                 app.craftingCellHeight, app.craftingCellWidth, 
                 app.craftingCellHeight, fill = None, borderWidth = 
                 app.cellBorderWidth, border = "black")
        drawLabel(app.toolList[x].name, app.craftingListTopLeft[0] + 
                  app.craftingCellWidth/2, app.craftingListTopLeft[1] + 
                  x * app.craftingCellHeight + 
                  app.craftingCellHeight/2)

def drawCraftWindow(app):
    #create window with list of possible items, each item in a cell. user can 
    #click a cell to try creating an item, and if they can create it, it is
    #added to their inventory and if not then a message saying they don't have
    #the necessary materials is displayed
    if app.craftedImpossible:
        drawLabel("Don't have necessary materials to craft", app.width/2, 200, size = 40)
    drawRect(app.width/2 + 300, app.height/2 - 250, 300, 500, fill = "white", 
             border = "black", borderWidth = 2 * app.cellBorderWidth)
    #draw close button
    drawRect(app.craftXButton[0], app.craftXButton[1], 
             app.craftXButton[2], app.craftXButton[3], 
             fill = "white", border = "black")
    drawLabel("X", app.craftXButton[0] + app.craftXButton[2]/2, 
              app.craftXButton[1] + app.craftXButton[3]/2, size = 50)
    drawCraftingCells(app)
    
def getDirection(app, startCell, endCell):
    direction = [endCell[0] - startCell[0], endCell[1] - startCell[1]]
    return direction

def moveToCell(app, startCell, endCell, dotIndex, cellWidth, cellHeight):
    direction = getDirection(app, startCell, endCell)
    app.dots[dotIndex].x += direction[1] * cellWidth
    app.dots[dotIndex].y += direction[0] * cellHeight

def makeAliensNextMove(app):
    numAliensFound = 0
    board = aStar.convertToBoard(app)
    cellWidth = app.width/app.boardRows
    cellHeight = app.height/app.boardCols
    destination = aStar.findCell(app.playerCoords[0], app.playerCoords[1], app.boardRows, 
                   app.boardCols, cellWidth, cellHeight)
    for x in range(len(app.dots)):
        #check if alien
        if isinstance(app.dots[x].hostObject, Alien) and app.dots[x].hostObject.health > 0:
            alienCoords = aStar.findCell(app.dots[x].x, app.dots[x].y, app.boardRows, 
                        app.boardCols, cellWidth, cellHeight)
            if alienCoords != None:
                path = aStar.aStar(board, destination, alienCoords)
                #move in direction of first cell in path
                if len(path) == 1: #then we're in the player's cell
                    numAliensFound += 1
                    app.playerHit = True
                    break
                if path != None:
                    moveToCell(app, alienCoords, path[1], x, cellWidth, cellHeight)
    if numAliensFound == 0:
        app.playerHit = False

def updateWindow(app, sign, direction):
    if direction == "x":
        app.planetDotGenerationWindow[0] += 5 * sign * app.player.currArmor.speedFactor
    else:
        app.planetDotGenerationWindow[1] += 5 * sign * app.player.currArmor.speedFactor

def updateDots(app, sign, direction):
    if direction == "x":
        for x in app.dots:
            x.x += 5 * sign * app.player.currArmor.speedFactor
        app.planetDotGenerationWindow[0] += 5 * sign * app.player.currArmor.speedFactor
    else:
        for x in app.dots:
            x.y += 5 * sign * app.player.currArmor.speedFactor
        app.planetDotGenerationWindow[1] += 5 * sign * app.player.currArmor.speedFactor

#all functions for planet scene
def planet_onKeyPress(app, key):
    if key == "space":
        setActiveScreen("solarSystem")
    elif key == "e":
        row = app.selectedRowCol[0]
        col = app.selectedRowCol[1]
        if app.player.inventory[row][col] != 0:
            if app.player.inventory[row][col][0] == 1:
                app.player.inventory[row][col] = 0
            else:
                app.player.inventory[row][col][0] -= 1
    elif key == "n" and app.gameOver:
        setActiveScreen("solarSystem")
        newGame(app)

def planet_onKeyHold(app, keys):
    if app.player.stamina > 0:
        if "a" in keys:
            if app.planetDotGenerationWindow[0] >= 0:
                if app.playerCoords[0] > 0:
                    app.playerCoords[0] -= 5 * app.player.currArmor.speedFactor     
                    updateWindow(app, +1, "x")
                    app.usePlayerCoordsX = True
                    app.player.stamina -= 1
                    app.stepCounter = 0
            elif app.usePlayerCoordsX:
                app.playerCoords[0] -= 5 * app.player.currArmor.speedFactor
                app.player.stamina -= 1
                app.stepCounter = 0
            else:
                updateDots(app, +1, "x")
                app.player.stamina -= 1
                app.stepCounter = 0
        if "s" in keys: 
            if app.planetDotGenerationWindow[1] + app.planetDotGenerationWindow[3] <= app.height:
                if app.playerCoords[1] < app.height:
                    app.playerCoords[1] += 5 * app.player.currArmor.speedFactor     
                    updateWindow(app, -1, "y")
                    app.usePlayerCoordsY = True
                    app.player.stamina -= 1
                    app.stepCounter = 0
            elif app.usePlayerCoordsY:
                app.playerCoords[1] += 5 * app.player.currArmor.speedFactor
                app.player.stamina -= 1
                app.stepCounter = 0
            else:
                updateDots(app, -1, "y")
                app.player.stamina -= 1
                app.stepCounter = 0
        if "w" in keys:
            if app.planetDotGenerationWindow[1] >= 0:
                if app.playerCoords[1] > 0:
                    app.playerCoords[1] -= 5 * app.player.currArmor.speedFactor     
                    updateWindow(app, +1, "y")
                    app.usePlayerCoordsY = True
                    app.player.stamina -= 1
                    app.stepCounter = 0
            elif app.usePlayerCoordsY:
                app.playerCoords[1] -= 5 * app.player.currArmor.speedFactor
                app.player.stamina -= 1
                app.stepCounter = 0
            else:
                updateDots(app, +1, "y")
                app.player.stamina -= 1
                app.stepCounter = 0
        if "d" in keys:
            if app.planetDotGenerationWindow[0] + app.planetDotGenerationWindow[2] <= app.width:
                if app.playerCoords[0] < app.width:
                    app.playerCoords[0] += 5 * app.player.currArmor.speedFactor     
                    updateWindow(app, -1, "x")
                    app.usePlayerCoordsX = True
                    app.player.stamina -= 1
                    app.stepCounter = 0
            elif app.usePlayerCoordsX:
                app.playerCoords[0] += 5 * app.player.currArmor.speedFactor 
                app.player.stamina -= 1
                app.stepCounter = 0
            else:
                updateDots(app, -1, "x")
                app.player.stamina -= 1
                app.stepCounter = 0
    if app.playerCoords[0] == app.width/2: 
        app.usePlayerCoordsX = False
    if app.playerCoords[1] == app.height/2:
        app.usePlayerCoordsY = False


def checkInventoryIconPress(app, mouseX, mouseY):
    xCoordIcon = app.inventoryIconCoords[0]
    yCoordIcon = app.inventoryIconCoords[1]
    widthIcon = app.inventoryIconCoords[2]
    heightIcon = app.inventoryIconCoords[3]
    if (xCoordIcon < mouseX < xCoordIcon + widthIcon) and (yCoordIcon < 
                                                             mouseY < yCoordIcon 
                                                             + heightIcon):
        return True
    
def checkCloseButtonPress(app, mouseX, mouseY):
    xCoordCloseButton = app.inventoryXButton[0]
    yCoordCloseButton = app.inventoryXButton[1]
    widthCloseButton = app.inventoryXButton[2]
    heightCloseButton = app.inventoryXButton[3]
    if app.inventoryPressed and (xCoordCloseButton - widthCloseButton/2 < 
                                 mouseX < xCoordCloseButton + 
                                 widthCloseButton/2) and (yCoordCloseButton - 
                                                          widthCloseButton/2 < 
                                                          mouseY < 
                                                          yCoordCloseButton + 
                                                          heightCloseButton/2):
        return True

def equipButtonPress(app, mouseX, mouseY):
    xCoordEquipButton = app.inventoryEquipButton[0]
    yCoordEquipButton = app.inventoryEquipButton[1] 
    widthEquipButton = app.inventoryEquipButton[2]
    heightEquipButton = app.inventoryEquipButton[3]
    if app.inventoryPressed and (xCoordEquipButton < mouseX < xCoordEquipButton + 
          widthEquipButton) and (yCoordEquipButton < mouseY < yCoordEquipButton 
                                 + heightEquipButton):
        return True

def equipCloseButtonPress(app, mouseX, mouseY):
    xCoordEquipX = app.equipXButton[0]
    yCoordEquipX = app.equipXButton[1]
    widthEquipX = app.equipXButton[2]
    heightEquipX = app.equipXButton[3]
    if app.equipPressed and (xCoordEquipX < mouseX < xCoordEquipX + 
                               widthEquipX) and (yCoordEquipX < mouseY < 
                                                 yCoordEquipX + heightEquipX):
        return True

def craftButtonPress(app, mouseX, mouseY):
    xCoordCraftButton = app.inventoryCraftButton[0]
    yCoordCraftButton = app.inventoryCraftButton[1]
    widthCraftButton = app.inventoryCraftButton[2]
    heightCraftButton = app.inventoryCraftButton[3]
    if app.inventoryPressed and (xCoordCraftButton < mouseX < xCoordCraftButton + 
          widthCraftButton) and (yCoordCraftButton < mouseY < yCoordCraftButton 
                                 + heightCraftButton):
        return True
    
def cellSelector(app, mouseX, mouseY, cellRow, cellCol):
    if (app.inventoryPressed) and (cellRow, cellCol) != (app.selectedRowCol
                                                           ) and (0 <= cellRow < 
                                                       app.inventoryRows) and (
                                                           0 <= cellCol < 
                                                           app.inventoryCols):
        return True

def cellDeselector(app, mouseX, mouseY, cellWidth, cellHeight):
    if app.selectedRowCol != None and app.inventoryPressed:
        selectedColLeftX = app.inventoryGridTopLeft[0] + cellWidth * app.selectedRowCol[1]
        selectedColLeftY = app.inventoryGridTopLeft[1] + cellWidth * app.selectedRowCol[0]
        if (selectedColLeftX < mouseX < selectedColLeftX + cellWidth) and (
            selectedColLeftY < mouseY < selectedColLeftY + cellHeight):
            return True
        
def dotClicked(app):
    if not app.inventoryPressed:
        #some negative
        minDistance = -1
        #some int
        minDot = 3
        for x in app.dots:
            pendingDistance = distance(x.x, x.y, app.width/2, app.height/2)
            if pendingDistance < app.player.currTool.hitRadius:
                if pendingDistance < minDistance or minDistance == -1:
                    if isinstance(x.hostObject, Material):
                        minDistance = pendingDistance
                        minDot = x
                    #can only interact with living Aliens
                    elif isinstance(x.hostObject, Alien) and x.hostObject.health > 0:
                        minDistance = pendingDistance
                        minDot = x
        if minDot != 3:
            return (True, minDot.hostObject)
        
def emptyCell(app, mouseX, mouseY):
    if app.inventoryPressed and app.selectedRowCol != None:
        #check if click was not inside the inventory window
        if (mouseX < app.width/2 - 250 or mouseX > app.width/2 + 250) or (mouseY
            < app.height/2 - 250 or mouseY > app.height/2 + 250):
            return True

def findRightInventoryCell(app, material):
    for x in range(len(app.player.inventory)):
        for y in range(len(app.player.inventory[0])):
            if app.player.inventory[x][y] != 0:
                #check if this inventory slot has the same material as what we want to add
                #and that the current amount is less than the stacking number for that material
                if app.player.inventory[x][y][1] == material and app.player.inventory[
                    x][y][0] < material.stackNumber:
                    return (x, y)
    return findNextEmptyCell(app)

def craftCloseButtonPress(app, mouseX, mouseY):
    xCoordCraftX = app.craftXButton[0]
    yCoordCraftX = app.craftXButton[1]
    widthCraftX = app.craftXButton[2]
    heightCraftX = app.craftXButton[3]
    if app.craftPressed and (xCoordCraftX < mouseX < xCoordCraftX + 
                               widthCraftX) and (yCoordCraftX < mouseY < 
                                                 yCoordCraftX + heightCraftX):
        return True

def craftCellSelector(app, mouseX, mouseY):
    cellRow = (mouseY - app.craftingListTopLeft[1]) // app.craftingCellHeight 
    if (app.craftingListTopLeft[0] < mouseX < app.craftingListTopLeft[0] + 
        app.craftingCellWidth) and app.craftPressed:
        if 0 <= cellRow < len(app.toolList) - 1:
            return (True, app.toolList[cellRow])

def ableToCraft(app, tool):
    woodTotal = 0
    metalTotal = 0
    for x in app.player.inventory:
        for y in x:
            if y == 0:
                continue
            if y[1] == app.wood:
                woodTotal += y[0]
            if y[1] == app.metal:
                metalTotal += y[0]
            if woodTotal >= tool.recipe[app.wood] and metalTotal >= tool.recipe[app.metal]:
                return True
    return False

def subtractMaterials(app, recipe):
    remainingMaterials = copy.copy(recipe)
    for x in range(len(app.player.inventory)):
        for y in range(len(app.player.inventory[x])):
            pendingCell = app.player.inventory[x][y]
            if pendingCell == 0:
                continue
            pendingCellMaterial = pendingCell[1]
            if pendingCellMaterial in recipe and remainingMaterials[pendingCellMaterial] > 0:
                #if there is more or the same of this material in the cell 
                #than what the recipe demands, take all the recipe demands
                #from the cell
                if pendingCell[0] >= remainingMaterials[pendingCellMaterial]:
                    pendingCell[0] -= remainingMaterials[pendingCellMaterial]
                    if pendingCell[0] == 0:
                        app.player.inventory[x][y] = 0
                    remainingMaterials[pendingCellMaterial] = 0
                else:
                    remainingMaterials[y[1]] -= y[0]
                    app.player.inventory[x][y] = 0

def findNextEmptyCell(app):
    nextEmptyCell = None
    for x in range(len(app.player.inventory)):
        for y in range(len(app.player.inventory[0])):
            if app.player.inventory[x][y] == 0:
                nextEmptyCell = (x, y)
                break
        if nextEmptyCell:
            break
    return nextEmptyCell

def addTool(app, tool):
    nextEmptyCell = findNextEmptyCell(app)
    app.player.inventory[nextEmptyCell[0]][nextEmptyCell[1]] = [1, tool]
    
def equipToolButtonPress(app, mouseX, mouseY):
    widthEquipToolButton = app.equipToolButton[2]
    heightEquipToolButton = app.equipToolButton[3]
    xCoordEquipToolButton = app.equipToolButton[0] - widthEquipToolButton/2
    yCoordEquipToolButton = app.equipToolButton[1] - heightEquipToolButton/2
    if app.equipPressed and (xCoordEquipToolButton < mouseX < xCoordEquipToolButton + 
          widthEquipToolButton) and (yCoordEquipToolButton < mouseY < yCoordEquipToolButton 
                                 + heightEquipToolButton):
        return True and app.selectedRowCol != None

def returnToolToInventoryButtonPress(app, mouseX, mouseY):
    widthUnequipToolButton = app.unequipToolButton[2]
    heightUnequipToolButton = app.unequipToolButton[3]
    xCoordUnequipToolButton = app.unequipToolButton[0] - widthUnequipToolButton/2
    yCoordUnequipToolButton = app.unequipToolButton[1] - heightUnequipToolButton/2
    if app.equipPressed and (xCoordUnequipToolButton < mouseX < xCoordUnequipToolButton + 
          widthUnequipToolButton) and (yCoordUnequipToolButton < mouseY < yCoordUnequipToolButton 
                                 + heightUnequipToolButton):
        return True

def planet_onStep(app):
    if not app.paused:
        if app.player.health == 0:
            app.gameOver = True
            app.paused = True
        if app.playerHit and app.counter % 10 == 0:
            app.player.health -= 1
        if app.counter % 10 == 0:
            app.counter = 0
            makeAliensNextMove(app)
        if app.stepCounter >= 50 and app.player.stamina < 100:
            app.player.stamina += 1
        app.counter += 1
        app.stepCounter += 1

def planet_onMousePress(app, mouseX, mouseY):
    cellWidth = app.inventoryGridWidth/app.inventoryCols
    cellHeight = app.inventoryGridHeight/app.inventoryRows
    cellCol = (mouseX - app.inventoryGridTopLeft[0]) // cellWidth
    cellRow = (mouseY - app.inventoryGridTopLeft[1]) // cellHeight
    if checkCloseButtonPress(app, mouseX, mouseY):
        app.inventoryPressed = False
    elif checkInventoryIconPress(app, mouseX, mouseY):
        app.inventoryPressed = True
    elif equipButtonPress(app, mouseX, mouseY):
        app.equipPressed = True
    elif equipCloseButtonPress(app, mouseX, mouseY):
        app.equipPressed = False
    elif equipToolButtonPress(app, mouseX, mouseY):
        if app.player.currTool != app.hand:
            nextEmptyCell = findNextEmptyCell(app)
            if nextEmptyCell != None:
                app.player.inventory[nextEmptyCell[0]][nextEmptyCell[1]] = [1, app.player.currTool]
        toolInSelectedCell = app.player.inventory[app.selectedRowCol[0]][app.selectedRowCol[1]][1]
        app.player.currTool = toolInSelectedCell
        app.player.inventory[app.selectedRowCol[0]][app.selectedRowCol[1]] = 0
    elif returnToolToInventoryButtonPress(app, mouseX, mouseY):
        nextEmptyCell = findNextEmptyCell(app)
        if nextEmptyCell != None:
            app.player.inventory[nextEmptyCell[0]][nextEmptyCell[1]] = [1, app.player.currTool]
        app.player.currTool = app.hand
    elif craftCloseButtonPress(app, mouseX, mouseY):
        app.craftPressed = False
    elif craftButtonPress(app, mouseX, mouseY):
        app.craftPressed = True
    elif cellSelector(app, mouseX, mouseY, cellRow, cellCol):
        app.selectedRowCol = (int(cellRow), int(cellCol))
    #deselect if they press the same one again
    elif cellDeselector(app, mouseX, mouseY, cellWidth, cellHeight):
        app.selectedRowCol = None
    elif dotClicked(app) != None:
            clickedDot = dotClicked(app)
            #if alien then deal damage to alien, and 
            if isinstance(clickedDot[1], Alien):
                clickedDot[1].health -= app.player.currTool.damage
            #if material collect material
            if isinstance(clickedDot[1], Material):
                pendingCell = findRightInventoryCell(app, clickedDot[1])
                #increase selected inventory slot by appropriate total 
                collectionFactor = app.player.currTool.efficiencyDict[clickedDot[1]]
                if pendingCell != None:
                    x = 0
                    while x < collectionFactor:
                        pendingCell = findRightInventoryCell(app, clickedDot[1])
                        if pendingCell != None:
                            pendingInventorySlot = app.player.inventory[pendingCell[0]][pendingCell[1]]
                            if isinstance(pendingInventorySlot, int):
                                app.player.inventory[pendingCell[0]][pendingCell[1]] = [1, clickedDot[1]]
                            else:
                                app.player.inventory[pendingCell[0]][pendingCell[1]][0] += 1         
                        x += 1    
    elif emptyCell(app, mouseX, mouseY):
        app.player.inventory[app.selectedRowCol[0]][app.selectedRowCol[1]] = 0
    elif craftCellSelector(app, mouseX, mouseY):
        pendingTool = craftCellSelector(app, mouseX, mouseY)[1]
        if ableToCraft(app, pendingTool):
            subtractMaterials(app, pendingTool.recipe)
            addTool(app, pendingTool)
        else:
            app.craftedImpossible = True

#conceptual understanding of side scrolling implementation learned from demo 
#provided by CMU professor Mike Taylor
#heavily heavily modified from demo, but technically I did learn the basics
#from it
#https://piazza.com/class/lkq6ivek5cg1bc/post/2231
def planet_redrawAll(app):
    #draw player at center, or playerCoords if usePlayerCoords is True
    drawRect(0, 0, app.width, app.height, fill = app.planet.backgroundColor)
    drawImage(app.playerImage, app.playerCoords[0] - app.playerSize/2, 
              app.playerCoords[1] - app.playerSize/2, width = app.playerSize, 
              height = app.playerSize)
    #a given element in app.dots is an instance of the Dot class with attributes 
    #x, y, size 
    for x in app.dots:
        #draw dots
        if 0 < x.x < app.width and 0 < x.y < app.height:
            if isinstance(x.hostObject, Alien):
                if x.hostObject.health > 0:
                    x.draw()
            else:
                x.draw()
    if app.inventoryPressed:
        drawInventory(app)
    if app.equipPressed:
        drawEquipWindow(app)
    if app.craftPressed:
        drawCraftWindow(app)
    #draw inventory icon
    drawInventoryIcon(app)
    #draw stamina and health if they are hit with aliens
    drawLabel(f"Stamina: {app.player.stamina}", 
                  app.healthLabel[0], app.healthLabel[1] + 50, size = 30)
    if app.playerHit:
        drawLabel(f"Health dropping! Run away! Health: {app.player.health}", 
                  app.healthLabel[0], app.healthLabel[1], size = 50)
    #check if game over
    if app.gameOver:
        drawLabel("Game Over! Health reached 0, press n to start new game", 
                  app.width/2, app.height/2, size = 60)
        


#all functions for solarSystem scene
def solarSystem_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = "black")
    app.solarSystem.draw(app.angles)
    if isinstance(app.selectedPlanet, int):
        drawLabel("You've selected Planet" + str(app.selectedPlanet) + 
                  " Click again to deselect, or press enter to visit it", 
                  app.width/2, 70, size = 40, fill = "white")
    else:
        drawLabel("Click to select a planet. The largest orbit your click is" + 
                  " outside of will be the planet you select.", app.width/2, 70, 
                  size = 40, fill = "white")

def solarSystem_onStep(app):
    for x in range(len(app.angles)):
        app.angles[x] += app.rotateSpeeds[x]

def solarSystem_onMousePress(app, mouseX, mouseY):
    #finding smallest ring that their click was within, and selecting the corresponding planet
    #deselect if they click when something is selected
    if isinstance(app.selectedPlanet, int):
        app.selectedPlanet = None
        app.planet = None
        app.dots = None
    else:
        maxX = 0
        for x in range(1, len(app.solarSystem.planets) + 1):
            if distance(mouseX, mouseY, app.solarSystem.centerX, 
                    app.solarSystem.centerY) > x * app.solarSystem.stepSize:
                if x > maxX:
                    maxX = x
        if maxX != 0: 
            app.selectedPlanet = maxX
            app.planet = app.planets[app.selectedPlanet - 1]
            app.dots = app.planet.generateDots()


#conceptual understanding of multiple screens implementation learned from demo 
#provided by CMU professor Mike Taylor
#https://piazza.com/class/lkq6ivek5cg1bc/post/2231
def solarSystem_onKeyPress(app, key):
    if key == "enter" and isinstance(app.selectedPlanet, int):
        setActiveScreen("planet")

runAppWithScreens(initialScreen = "solarSystem", width = 1900, height = 1000)