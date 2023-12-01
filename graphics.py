from cmu_graphics import *
import random
from planet import Planet
import math
from solarSystem import solarSystem
from materials import Material
from player import Player
from tool import Tool
from armour import Armour

#To - do
#Collecting materials and storing in inventory and emptying cells in inventory
#pending functions: drawCraftWindow, what to do with third button in inventory

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


#materials 
wood = Material((lightBrown, darkBrown), 10, 30)
metal = Material((gray, sand), 10, 30)

#tools
axe = Tool(8, 10, 1, 1, "axe")
pickaxe = Tool(3, 1, 10, 1, "pickaxe")
sword = Tool(5, 1, 1, 3, "sword")
hand = Tool(1, 1, 1, 1, "hand")

#armours
skin = Armour(1, 1, "skin")


#onAppStart for all scenes
def onAppStart(app):
    app.player = Player()
    app.player.currTool = hand
    app.player.currArmor = skin
    app.scrollX = 0
    app.scrollY = 0
    app.planets = [Planet("green", 30, app.width, app.height, (wood, metal)), 
                   Planet("blue", 30, app.width, app.height, (wood, metal)), 
                   Planet("purple", 30, app.width, app.height, (wood, metal))]
    app.solarSystem = solarSystem(app.planets, app.width/2, app.height/2) 
    app.planet = None
    app.dots = None
    app.rotateSpeeds = [random.uniform(0, 0.5) for x in range(len(app.solarSystem.planets))]
    app.angles = [1 for x in range(len(app.solarSystem.planets))]
    app.selectedPlanet = None
    app.inventoryIconCoords = (50, 850, 100, 100)
    app.inventoryXButton = (app.width/2 + 200, app.height/2 - 200, 50, 50)
    app.inventoryCraftButton = (app.width/2 - 200, app.height/2 - 75, 100, 50)
    app.inventoryEquipButton = (app.width/2 - 50, app.height/2 - 75, 100, 50)
    app.inventoryThirdButton = (app.width/2 + 100, app.height/2 - 75, 100, 50)
    app.inventoryPressed = False
    app.inventoryGridTopLeft = (app.width/2 - 200, app.height/2)
    app.inventoryCols = app.player.inventoryCols
    app.inventoryRows = app.player.inventoryRows
    app.inventoryGridWidth = 400
    app.inventoryGridHeight = 200
    app.inventory = app.player.inventory
    app.cellBorderWidth = 2
    app.equipPressed = False
    app.selectedRowCol = None
    app.thirdButtonPressed = False
    app.craftPressed = False
    app.equipXButton = (575, 275, 50, 50)

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
    if content == None:
        drawLabel("empty", cellLeft + cellWidth/2, cellTop + cellWidth/2)
    else:
        drawLabel(content, cellLeft + cellWidth/2, cellTop + cellWidth/2)

def drawInventoryGrid(app):
    for y in range(app.inventoryRows):
        for x in range(app.inventoryCols):
            drawCell(app, y, x, app.inventory[y][x])
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
    #draw select button cell
    drawRect(app.inventoryThirdButton[0], app.inventoryThirdButton[1], 
             app.inventoryThirdButton[2], app.inventoryThirdButton[3],
             fill = None, border = "black", borderWidth = app.cellBorderWidth)
    drawLabel("Third Button", app.inventoryThirdButton[0] + 
              app.inventoryThirdButton[2]/2, app.inventoryThirdButton[1] + 
              app.inventoryThirdButton[3]/2)

def drawInventory(app):
    drawRect(app.width/2, app.height/2, 500, 500, align = "center", 
             fill = "white", border = "black", 
             borderWidth = 2 * app.cellBorderWidth)
    drawLabel("Inventory", app.width/2, app.height/2 - 150, size = 100)
    drawLabel("Click on a cell to select. Click outside to empty. Press d" + 
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

def drawCraftWindow(app):
    #create window with list of possible items, each item in a cell. user can 
    #click a cell to try creating an item, and if they can create it, it is
    #added to their inventory and if not then a message saying they don't have
    #the necessary materials is displayed
    pass

#all functions for planet scene
def planet_onKeyPress(app, key):
    if key == "left" or key == "a":
        app.scrollX += 5
    elif key == "right" or key == "d":
        app.scrollX -= 5
    elif key == "up" or key == "w":
        app.scrollY += 5
    elif key == "down" or key == "s":
        app.scrollY -= 5
    elif key == "space":
        setActiveScreen("solarSystem")

def planet_onKeyHold(app, keys):
    if "left" in keys:
        app.scrollX += 5
    if "right" in keys:
        app.scrollX -= 5
    if "up" in keys:
        app.scrollY += 5
    if "down" in keys:
        app.scrollY -= 5    

def planet_onMousePress(app, mouseX, mouseY):
    xCoordIcon = app.inventoryIconCoords[0]
    yCoordIcon = app.inventoryIconCoords[1]
    widthIcon = app.inventoryIconCoords[2]
    heightIcon = app.inventoryIconCoords[3]
    xCoordCloseButton = app.inventoryXButton[0]
    yCoordCloseButton = app.inventoryXButton[1]
    widthCloseButton = app.inventoryXButton[2]
    heightCloseButton = app.inventoryXButton[3]
    xCoordEquipButton = app.inventoryEquipButton[0]
    yCoordEquipButton = app.inventoryEquipButton[1] 
    widthEquipButton = app.inventoryEquipButton[2]
    heightEquipButton = app.inventoryEquipButton[3]
    xCoordThirdButton = app.inventoryThirdButton[0]
    yCoordThirdButton = app.inventoryThirdButton[1]
    widthThirdButton = app.inventoryThirdButton[2]
    heightThirdButton = app.inventoryThirdButton[3]
    xCoordCraftButton = app.inventoryCraftButton[0]
    yCoordCraftButton = app.inventoryCraftButton[1]
    widthCraftButton = app.inventoryCraftButton[2]
    heightCraftButton = app.inventoryCraftButton[3]
    xCoordEquipX = app.equipXButton[0]
    yCoordEquipX = app.equipXButton[1]
    widthEquipX = app.equipXButton[2]
    heightEquipX = app.equipXButton[3]
    if app.inventoryPressed and (xCoordCloseButton - widthCloseButton/2 < 
                                 mouseX < xCoordCloseButton + 
                                 widthCloseButton/2) and (yCoordCloseButton - 
                                                          widthCloseButton/2 < 
                                                          mouseY < 
                                                          yCoordCloseButton + 
                                                          heightCloseButton/2):
        app.inventoryPressed = False
    elif (xCoordIcon < mouseX < xCoordIcon + widthIcon) and (yCoordIcon < 
                                                             mouseY < yCoordIcon 
                                                             + heightIcon):
        app.inventoryPressed = True
    elif (xCoordEquipButton < mouseX < xCoordEquipButton + 
          widthEquipButton) and (yCoordEquipButton < mouseY < yCoordEquipButton 
                                 + heightEquipButton):
        app.equipPressed = True
    elif app.equipPressed and (xCoordEquipX < mouseX < xCoordEquipX + 
                               widthEquipX) and (yCoordEquipX < mouseY < 
                                                 yCoordEquipX + heightEquipX):
        app.equipPressed = False
    elif (xCoordThirdButton < mouseX < xCoordThirdButton + 
          widthThirdButton) and (yCoordThirdButton < mouseY < yCoordThirdButton 
                                 + heightThirdButton):
        app.thirdButtonPressed = True
    elif (xCoordCraftButton < mouseX < xCoordCraftButton + 
          widthCraftButton) and (yCoordCraftButton < mouseY < yCoordCraftButton 
                                 + heightCraftButton):
        app.craftPressed = True
    cellWidth = app.inventoryGridWidth/app.inventoryCols
    cellHeight = app.inventoryGridHeight/app.inventoryRows
    cellCol = (mouseX - app.inventoryGridTopLeft[0]) // cellWidth
    cellRow = (mouseY - app.inventoryGridTopLeft[1]) // cellHeight
    if (0 <= cellRow < app.inventoryRows) and (0 <= cellCol < 
                                               app.inventoryCols) and (
                                                   app.selectedRowCol == None):
        app.selectedRowCol = (cellRow, cellCol)
    #deselect if they press the same one again
    elif app.selectedRowCol != None:
        selectedColLeftX = app.inventoryGridTopLeft[0] + cellWidth * app.selectedRowCol[1]
        selectedColLeftY = app.inventoryGridTopLeft[1] + cellWidth * app.selectedRowCol[0]
        if (selectedColLeftX < mouseX < selectedColLeftX + cellWidth) and (
            selectedColLeftY < mouseY < selectedColLeftY + cellHeight):
            app.selectedRowCol = None
    
#conceptual understanding of side scrolling implementation learned from demo 
#provided by CMU professor Mike Taylor
#https://piazza.com/class/lkq6ivek5cg1bc/post/2231
def planet_redrawAll(app):
    xValue = app.width/2
    yValue = app.height/2
    #draw player at center
    drawRect(0, 0, app.width, app.height, fill = app.planet.backgroundColor)
    drawCircle(xValue, yValue, 10, fill = "black")
    #a given element in app.dots is an instance of the Dot class with attributes 
    #x, y, size and color
    for x in app.dots:
        xCoord = x.x + app.scrollX
        yCoord = x.y + app.scrollY
        #draw dots
        drawCircle(xCoord, yCoord, x.size, fill = x.color)
    if app.inventoryPressed:
        drawInventory(app)
    if app.equipPressed:
        drawEquipWindow(app)
    if app.craftPressed:
        drawCraftWindow(app)
    #draw inventory icon
    drawInventoryIcon(app)

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