from cmu_graphics import *
import random
from planet import Planet
import math

#solar system class
class solarSystem:
    def __init__(self, planets, centerX, centerY):
        self.planets = planets
        self.centerX = centerX
        self.centerY = centerY
        self.biggestCircleRadius = 400
        self.stepSize = self.biggestCircleRadius/len(self.planets)
    
    #draws planet on a particular orbit line (basically draws things in polar coordinates with respect
    #to self.centerX and self.centerY)
    def drawPlanet(self, angle, radius, color):
        x = math.sin(angle) * radius + self.centerX
        y = self.centerY - math.cos(angle) * radius
        drawCircle(x, y, 10, fill = color)

    def draw(self, angles):
        #first, need to draw concentric circles representing an orbit
        #then, need to draw an animated planet for each orbit
        for x in range(len(self.planets)):
            if x == 0:
                drawCircle(self.centerX, self.centerY, self.stepSize, fill = None, border = "white")
                color = self.planets[x].backgroundColor
                self.drawPlanet(angles[x], self.stepSize, color)
                continue
            rad = (x + 1)*self.stepSize
            drawCircle(self.centerX, self.centerY, rad, fill = None, border = "white")
            color = self.planets[x].backgroundColor
            self.drawPlanet(angles[x], rad, color)

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#colors
darkGreen = rgb(0, 102, 0)
lightGreen = rgb(51, 204, 51)
darkBrown = rgb(102, 51, 0)
lightBrown = rgb(153, 102, 51)
middleGreen = rgb(0, 153, 51)
sand = rgb(194, 178, 128)

#onAppStart for all scenes
def onAppStart(app):
    app.scrollX = 0
    app.scrollY = 0
    app.planets = [Planet((darkGreen, "blue"), "green", 30, 5, 
                                         app.width, app.height), Planet(("green", "blue"), "blue", 30, 5, 
                                         app.width, app.height), Planet(("green", "blue"), "purple", 30, 5, 
                                         app.width, app.height)]
    app.solarSystem = solarSystem(app.planets, app.width/2, app.height/2) 
    app.planet = None
    app.dots = None
    app.rotateSpeeds = [random.uniform(0, 0.5) for x in range(len(app.solarSystem.planets))]
    app.angles = [1 for x in range(len(app.solarSystem.planets))]
    app.selectedPlanet = None

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

def planet_redrawAll(app):
    xValue = app.width/2
    yValue = app.height/2
    #draw player at center
    drawRect(0, 0, app.width, app.height, fill = app.planet.backgroundColor)
    drawCircle(xValue, yValue, 10, fill = "black")
    #a given element in app.dots is [x, y, color, size]
    for x in app.dots:
        xCoord = x[0] + app.scrollX
        yCoord = x[1] + app.scrollY
        #draw dots
        drawCircle(xCoord, yCoord, x[3], fill = x[2])

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

def solarSystem_onKeyPress(app, key):
    if key == "enter" and isinstance(app.selectedPlanet, int):
        setActiveScreen("planet")

runAppWithScreens(initialScreen = "solarSystem", width = 1900, height = 1000)