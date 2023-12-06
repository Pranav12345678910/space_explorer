from random import *
from dot import *
import copy
import voronoi

class Planet:
    #Planets are specifications to randomly generate dots
    def __init__(self, backgroundColor, numDots, generateWidth, generateHeight, 
                 appWidth, appHeight, possibleMaterials, numAliens, 
                 possibleAliens, seeds):
        self.backgroundColor = backgroundColor
        self.generateWidth = generateWidth
        self.generateHeight = generateHeight
        self.possibleMaterials = possibleMaterials
        self.appWidth = appWidth
        self.appHeight = appHeight
        self.numAliens = numAliens
        self.possibleAliens = possibleAliens
        self.numDots = numDots
        self.seeds = seeds
        self.seedDict = voronoi.generateRandomDict(self.seeds)
        self.tempSize = 3

    def generate(self):
        result = []
        for x in range(self.numDots):
            materialIndex = randint(0, len(self.possibleMaterials) - 1)
            widthRange = ((self.appWidth/2 - self.generateWidth/2), 
                          (self.generateWidth/2 + self.appWidth/2))
            heightRange = ((self.appHeight/2 - self.generateHeight/2), 
                           (self.generateHeight/2 + self.appHeight/2))
            result.append(self.possibleMaterials[materialIndex].
                          generateDot(widthRange, heightRange, self.tempSize))
        return result

    def generateDots(self):
        #returns a list of dots
        #uses voronoi noise for size
        result = self.generate()
        for x in result:
            #run this inner loop once for each dot we want to create
            materialIndex = randint(0, len(self.possibleMaterials) - 1)
            closeSeed = voronoi.getNearestSeed(self.seeds, x.x, x.y)
            dotSize = self.seedDict[closeSeed]
            x.size = dotSize
        for x in range(self.numAliens):
            alienIndex = randint(0, len(self.possibleAliens) - 1)
            widthRange = ((self.appWidth/2 - self.generateWidth/2), 
                          (self.generateWidth/2 + self.appWidth/2))
            heightRange = ((self.appHeight/2 - self.generateHeight/2), 
                           (self.generateHeight/2 + self.appHeight/2))
            result.append(copy.copy(self.possibleAliens[alienIndex]).
                          generateDot(widthRange, heightRange))
        return result