import numpy as np

def calculateReward(cars):
    cost = 0
    for c in cars:
        if c.action == c.STOP:
            cost -= 1
    return cost

def updatePositions(cars, lights):
    