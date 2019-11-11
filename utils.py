import numpy as np

def calculateReward(cars):
    cost = 0
    for c in cars:
        if c.stopped:
            cost -= 1
    return cost

# no longer
def pruneCars(cars):

