from random import *
from dot import *

class Planet:
    #Planets are specifications to randomly generate dots
    def __init__(self, backgroundColor, numDots, appWidth, appHeight, possibleMaterials):
        self.backgroundColor = backgroundColor
        self.numDots = numDots
        self.appWidth = appWidth
        self.appHeight = appHeight
        self.possibleMaterials = possibleMaterials


    def generateDots(self):
        #returns a list of dots, where each dot takes in x, y, color, size
        #first generates list of materials 
        result = []
        for x in range(self.numDots):
            materialIndex = randint(0, len(self.possibleMaterials) - 1)
            result.append(self.possibleMaterials[materialIndex].generateDot(self.appWidth, self.appHeight))
        return result