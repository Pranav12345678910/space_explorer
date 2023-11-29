from cmu_graphics import *

#blobs are the bits of materials that get drawn
#so that they can be drawn, dots must have a radius
class Dot:
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self):
        drawCircle(self.x, self.y, self.size, fill = self.color)
    


