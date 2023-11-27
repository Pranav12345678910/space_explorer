from planet import Planet 
from cmu_graphics import *
import random
import math

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