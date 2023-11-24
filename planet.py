import random

class Planet:
    #Planets, graphically, are just specifications to randomly generate dots (for now)
    def __init__(self, dotColors, backgroundColor, maxSize, numDots, appWidth, appHeight):
        self.dotColors = dotColors
        self.backgroundColor = backgroundColor
        self.maxSize = maxSize
        self.minSize = 10
        self.numDots = numDots
        self.appWidth = appWidth
        self.appHeight = appHeight


    def generateDots(self):
        #returns a list of dots, where each dot is a 4-tuple: (x, y, color, size)
        return [[random.randrange(self.appWidth), random.randrange(self.appHeight), 
                self.dotColors[random.randint(1, len(self.dotColors) - 1)], 
                random.randint(10, self.maxSize)] for _ in range(self.numDots)]