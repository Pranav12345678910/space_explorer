from random import *
from cmu_graphics import *


#dots are the visual representation of a bit of materials that gets drawn
#so that they can be drawn, dots must have all the information to draw: 
#x-coord, y-coord, size, color
class Dot:
    def __init__(self, x, y, size, image, hostObject):
        self.x = x
        self.y = y
        self.size = size
        self.image = image
        self.hostObject = hostObject

    def draw(self):
        drawImage(self.image, self.x - self.size/2, self.y - self.size/2, width 
                  = self.size, height = self.size)
    
    def __repr__(self):
        return f"Dot({self.x}, {self.y})"