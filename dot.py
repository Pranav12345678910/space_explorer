from random import *
from cmu_graphics import *


#dots are the visual representation of a bit of materials that gets drawn
#so that they can be drawn, dots must have all the information to draw: 
#x-coord, y-coord, size, color
class Dot:
    def __init__(self, x, y, color, size, materialName):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.materialName = materialName

    def draw(self):
        drawCircle(self.x, self.y, self.size, fill = self.color)
    
    def __repr__(self):
        return f"({self.x}, {self.y})"