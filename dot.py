from random import *
from cmu_graphics import *


#dots are the visual representation of a bit of materials that gets drawn
#so that they can be drawn, dots must have all the information to draw: 
#x-coord, y-coord, size, color
class Dot:
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self):
        drawCircle(self.x, self.y, self.size, fill = self.color)