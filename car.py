import utils
import numpy as np

class Car:
    """
    Car class - models behavior of cars
    """
    MAX_SPEED = 25

    def __init__(self):
        self.pos = # (x,y)
        self.speed = # bounded gaussian
        self.dir = # up down left right
        self.action = # straight left, right, stop
        self.follow_dist = # uniform dist
