import random
import math

#learned conceptual understanding from 
#https://www.ronja-tutorials.com/post/028-voronoi-noise/#summary
#first generate seeds
def getSeeds(xRange, yRange, numSeeds):
    seeds = []
    for x in range(numSeeds):
        x = random.randrange(*xRange)
        y = random.randrange(*yRange)
        seeds.append((x, y))
    return seeds

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def getNearestSeed(seeds, x, y):
    minSeed = seeds[0]
    #some negative
    minDistance = distance(*seeds[0], x, y)
    for x in range(1, len(seeds)):
        pendingDistance = distance(*seeds[x], x, y) 
        if pendingDistance < minDistance:
            minDistance = pendingDistance
            minSeed = seeds[x]
    return minSeed

#generates random dictionary mapping from particular seeds to a number of dots 
#to generate in that "zone", as well as the dot size for that "zone"
def generateRandomDict(seeds):
    resultDict = {}
    for x in seeds:
        #size of dots for that seed
        resultDict[x] = random.randint(10, 30)
    return resultDict

