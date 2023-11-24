from cmu_graphics import *
import random
from planet import Planet
from solarSystem import solarSystem

darkGreen = rgb(0, 102, 0)
lightGreen = rgb(51, 204, 51)
darkBrown = rgb(102, 51, 0)
lightBrown = rgb(153, 102, 51)
middleGreen = rgb(0, 153, 51)
sand = rgb(194, 178, 128)

def onAppStart(app):
    app.scrollX = 0
    app.scrollY = 0
    #dotColors, backgroundColor, size, numDots, appWidth, appHeight
    app.planet = Planet((darkGreen, lightBrown, darkBrown), middleGreen, 50, 30, 
                          app.width, app.height)
    app.dots = app.planet.generateDots()

def onKeyPress(app, key):
    if key == "left" or key == "a":
        app.scrollX += 5
    elif key == "right" or key == "d":
        app.scrollX -= 5
    elif key == "up" or key == "w":
        app.scrollY += 5
    elif key == "down" or key == "s":
        app.scrollY -= 5

def onKeyHold(app, keys):
    if "left" in keys:
        app.scrollX += 5
    if "right" in keys:
        app.scrollX -= 5
    if "up" in keys:
        app.scrollY += 5
    if "down" in keys:
        app.scrollY -= 5

def redrawAll(app):
    xValue = app.width/2
    yValue = app.height/2
    #draw player at center
    drawRect(0, 0, app.width, app.height, fill = "blue")
    drawCircle(xValue, yValue, 10, fill = "green")
    #a given element in app.dots is [x, y, color, size]
    for x in app.dots:
        xCoord = x[0] + app.scrollX
        yCoord = x[1] + app.scrollY
        #draw dots
        drawCircle(xCoord, yCoord, x[3], fill = x[2])

runApp(width = 1900, height = 1000)