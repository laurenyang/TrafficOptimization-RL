import utils
import numpy as np

class Car:
    """
    Car class - models behavior of cars
    """
    MAX_SPEED = 25

    # actions
    STOP = 0
    STRAIGHT = 1
    LEFT_TURN = 2
    RIGHT_TURN = 3

    # directions
    LEFT_DIR = 0
    UP_DIR = 1
    RIGHT_DIR = 2
    DOWN_DIR = 3

    def __init__(self, pos, speed, direction, action, follow_dist):
        self.pos = pos # (x,y)
        self.speed = speed # bounded gaussian
        self.dir = direction # up down left right
        self.action = action # straight left, right, stop
        self.follow_dist = follow_dist # uniform dist

    
