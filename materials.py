from random import *
import cmu_graphics
from dot import *

#a material just has a certain color, as well as graphical properties
#like a range of sizes
class Material:
    def __init__(self, dotColors, minSize, maxSize, name, stackNumber):
        self.minSize = minSize
        self.maxSize = maxSize
        self.dotColors = dotColors
        self.name = name
        self.stackNumber = stackNumber
    
    def generateDot(self, appWidth, appHeight):
        return Dot(randrange(appWidth), 
                   randrange(appHeight), 
                   self.dotColors[randint(0, len(self.dotColors) - 1)], 
                   randint(self.minSize, self.maxSize), self.name)