from random import *
from dot import *

class Planet:
    #Planets are specifications to randomly generate dots
    def __init__(self, backgroundColor, numDots, generateWidth, generateHeight, 
                 appWidth, appHeight, possibleMaterials):
        self.backgroundColor = backgroundColor
        self.numDots = numDots
        self.generateWidth = generateWidth
        self.generateHeight = generateHeight
        self.possibleMaterials = possibleMaterials
        self.appWidth = appWidth
        self.appHeight = appHeight


    def generateDots(self):
        #returns a list of dots, where each dot takes in x, y, color, size
        #first generates list of materials 
        result = []
        for x in range(self.numDots):
            materialIndex = randint(0, len(self.possibleMaterials) - 1)
            widthRange = ((self.appWidth/2 - self.generateWidth/2), (self.generateWidth/2 + self.appWidth/2))
            heightRange = ((self.appHeight/2 - self.generateHeight/2), (self.generateHeight/2 + self.appHeight/2))
            result.append(self.possibleMaterials[materialIndex].generateDot(widthRange, heightRange))
        return result