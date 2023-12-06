from random import *
import cmu_graphics
from dot import *

#a material just has a certain color, as well as graphical properties
#like a range of sizes
class Material:
    def __init__(self, minSize, maxSize, name, stackNumber, image):
        self.minSize = minSize
        self.maxSize = maxSize
        self.name = name
        self.stackNumber = stackNumber
        self.image = image
    
    def generateDot(self, widthRange, heightRange):
        return Dot(randrange(*widthRange), 
                   randrange(*heightRange), 
                   randint(self.minSize, self.maxSize), self.image, self)