from cmu_graphics import *
import random
from planet import Planet
import math
from solarSystem import solarSystem
from materials import Material

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



#onAppStart for all scenes
def onAppStart(app):
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
    app.inventoryPressed = False

def drawInventoryIcon(app):
    drawRect(*app.inventoryIconCoords, opacity = 30) 
    drawLabel("Inventory", 100, 900)   

def drawInventory(app):
    drawRect(app.width/2, app.height/2, 500, 500, align = "center", fill = "white")
    drawLabel("Inventory", app.width/2, app.height/2 - 175, size = 100)
    #find grid making code from tetris

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
    xCoord = app.inventoryIconCoords[0]
    yCoord = app.inventoryIconCoords[1]
    width = app.inventoryIconCoords[2]
    if app.inventoryPressed:
        app.inventoryPressed = False
    elif (xCoord < mouseX < xCoord + width) and (yCoord < mouseY < yCoord + width):
        app.inventoryPressed = True

#conceptual understanding of side scrolling implementation learned from demo 
#provided by CMU professor Mike Taylor
#https://piazza.com/class/lkq6ivek5cg1bc/post/2231
def planet_redrawAll(app):
    xValue = app.width/2
    yValue = app.height/2
    #draw player at center
    drawRect(0, 0, app.width, app.height, fill = app.planet.backgroundColor)
    drawCircle(xValue, yValue, 10, fill = "black")
    #a given element in app.dots is an instance of the Dot class with attributes x, y, size and color
    for x in app.dots:
        xCoord = x.x + app.scrollX
        yCoord = x.y + app.scrollY
        #draw dots
        drawCircle(xCoord, yCoord, x.size, fill = x.color)
    if app.inventoryPressed:
        drawInventory(app)
    #draw inventory icon
    drawInventoryIcon(app)

#all functions for solarSystem scene
def solarSystem_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = "black")
    app.solarSystem.draw(app.angles)
    if isinstance(app.selectedPlanet, int):
        drawLabel("You've selected Planet" + str(app.selectedPlanet) + " Click again to deselect, or press enter to visit it", app.width/2, 70, size = 40, fill = "white")
    else:
        drawLabel("Click to select a planet. The largest orbit your click is outside of will be the planet you select.", app.width/2, 70, size = 40, fill = "white")

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