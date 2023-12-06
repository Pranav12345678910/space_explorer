from random import *
from dot import Dot

class Alien:
    def __init__(self, tool, armour, image, size):
        self.health = 10
        self.tool = tool
        self.armour = armour
        self.image = image
        self.size = size
        self.moveSpeed = 30

    def generateDot(self, widthRange, heightRange):
        return Dot(randrange(*widthRange), 
                randrange(*heightRange), self.size, self.image, self)
