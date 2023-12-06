from random import *
from dot import *
import copy

class Planet:
    #Planets are specifications to randomly generate dots
    def __init__(self, backgroundColor, numDots, generateWidth, generateHeight, 
                 appWidth, appHeight, possibleMaterials, numAliens, possibleAliens):
        self.backgroundColor = backgroundColor
        self.numDots = numDots
        self.generateWidth = generateWidth
        self.generateHeight = generateHeight
        self.possibleMaterials = possibleMaterials
        self.appWidth = appWidth
        self.appHeight = appHeight
        self.numAliens = numAliens
        self.possibleAliens = possibleAliens


    def generateDots(self):
        #returns a list of dots, where each dot takes in x, y, color, size
        #first generates list of materials 
        result = []
        for x in range(self.numDots):
            materialIndex = randint(0, len(self.possibleMaterials) - 1)
            widthRange = ((self.appWidth/2 - self.generateWidth/2), 
                          (self.generateWidth/2 + self.appWidth/2))
            heightRange = ((self.appHeight/2 - self.generateHeight/2), 
                           (self.generateHeight/2 + self.appHeight/2))
            result.append(self.possibleMaterials[materialIndex].
                          generateDot(widthRange, heightRange))
        for x in range(self.numAliens):
            alienIndex = randint(0, len(self.possibleAliens) - 1)
            widthRange = ((self.appWidth/2 - self.generateWidth/2), 
                          (self.generateWidth/2 + self.appWidth/2))
            heightRange = ((self.appHeight/2 - self.generateHeight/2), 
                           (self.generateHeight/2 + self.appHeight/2))
            result.append(copy.copy(self.possibleAliens[alienIndex]).
                          generateDot(widthRange, heightRange))
        return result