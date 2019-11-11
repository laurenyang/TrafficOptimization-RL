import numpy as np

def calculateReward(cars):
    cost = 0
    for c in cars:
        if c.stopped:
            cost -= 1
    return cost

# no longer consider cars that are past 
def pruneCars(cars):

    newCars = []
    for c in cars:
        prune = False
        prune |= c.dir == c.LEFT_DIR and c.pos[0] < 0
        prune |= c.dir == c.UP_DIR and c.pos[1] > 0
        prune |= c.dir == c.RIGHT_DIR and c.pos[0] > 0
        prune |= c.dir == c.DOWN_DIR and c.pos[1] < 0

        if not prune:
            newCars.append(c)
    
    return newCars
