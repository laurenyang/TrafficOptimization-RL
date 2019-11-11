import utils
from car import *
import numpy as np
import copy
import random
import scipy.stats

class CarGenerator:
    # speed limit in mph
    MAX_SPEED = 25

    # distance in miles
    INTERSECTION_LENGTH = 0.25

    AVG_ACCELERATION = 0.001

    # directions
    LEFT_DIR = 0
    UP_DIR = 1
    RIGHT_DIR = 2
    DOWN_DIR = 3
    MIN_TIME_BETWEEN_CARS = 5

    def __init__(self, direction, p):
        # direction
        self.direction = direction
        self.p = p
        self.prev_time = 0


    def gen_car(self, t):
        if np.random.binomial(1, self.p) == 0 and t < self.prev_time + self.MIN_TIME_BETWEEN_CARS:
            return None

        self.prev_time = t

        # truncated normal from 15 to 40 mph
        speed = scipy.stats.truncnorm.rvs(-10 / 2.5, 15/2.5, loc=25, scale=2.5, size=1)[0]

        # may not use this
        follow_dist = 20 / 5280

        if self.direction == self.LEFT_DIR:
            car = Car([self.INTERSECTION_LENGTH, 0], speed, AVG_ACCELERATION, self.LEFT_DIR, random.randint(1, 3), follow_dist)
        elif self.direction == self.RIGHT_DIR:
            car = Car([-self.INTERSECTION_LENGTH, 0], speed, AVG_ACCELERATION, self.RIGHT_DIR, random.randint(1, 3), follow_dist)
        elif self.direction == self.UP_DIR:
            car = Car([0, self.INTERSECTION_LENGTH], speed, AVG_ACCELERATION, self.UP_DIR, random.randint(1, 3), follow_dist)
        elif self.direction == self.DOWN_DIR:
            car = Car([0, -self.INTERSECTION_LENGTH], speed, AVG_ACCELERATION, self.DOWN_DIR, random.randint(1, 3), follow_dist)

        return car