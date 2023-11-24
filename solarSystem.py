from planet import Planet
from cmu_graphics import *
import random
import math

def onAppStart(app):
    app.solarSystem = solarSystem([Planet(("green", "blue"), "green", 30, 5, 
                                         app.width, app.height), Planet(("green", "blue"), "blue", 30, 5, 
                                         app.width, app.height), Planet(("green", "blue"), "purple", 30, 5, 
                                         app.width, app.height)], app.width/2, app.height/2) 
    app.rotateSpeeds = [random.uniform(0, 0.5) for x in range(len(app.solarSystem.planets))]
    app.angles = [1 for x in range(len(app.solarSystem.planets))]

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = "black")
    app.solarSystem.draw(app.angles)

def onStep(app):
    for x in range(len(app.angles)):
        app.angles[x] += app.rotateSpeeds[x]

class solarSystem:
    def __init__(self, planets, centerX, centerY):
        self.planets = planets
        self.centerX = centerX
        self.centerY = centerY
        self.biggestCircleRadius = 500
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
                drawCircle(self.centerX, self.centerY, 40, fill = None, border = "white")
                color = self.planets[x].backgroundColor
                self.drawPlanet(angles[x], 40, color)
                continue
            rad = 40 + x*self.stepSize
            drawCircle(self.centerX, self.centerY, rad, fill = None, border = "white")
            color = self.planets[x].backgroundColor
            self.drawPlanet(angles[x], rad, color)

runApp(width = 1900, height = 1000)
    