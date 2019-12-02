import utils
from car import *
import numpy as np
import copy
import random
import scipy.stats

class CarGenerator:
    # speed limit in mph
    MAX_SPEED = 25
    MAX_SPEED = 30 / 3600 # miles per second

    # distance in miles
    INTERSECTION_LENGTH = 0.25

    AVG_ACCELERATION = MAX_SPEED / 2.0 # two seconds from stop to full speed

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
        self.prev_time = -1000


    def gen_car(self, t):
        choice = np.random.binomial(1, self.p)
        # print(t, choice, self.prev_time)

        if choice == 0 or t < self.prev_time + self.MIN_TIME_BETWEEN_CARS:
            return None
        # print('new car generated')
        self.prev_time = t

        # truncated normal from 15 to 40 mph
        speed = (scipy.stats.truncnorm.rvs(-10 / 2.5, 15/2.5, loc=25, scale=2.5, size=1)[0]) / 3600

        speed = 30 / 3600

        # may not use this
        follow_dist = 80 / 5280


        # cars should not be accelerating
        if self.direction == self.LEFT_DIR:
            car = Car([self.INTERSECTION_LENGTH, 0], speed, 0, self.LEFT_DIR, random.randint(1, 3), follow_dist)
        elif self.direction == self.RIGHT_DIR:
            car = Car([-self.INTERSECTION_LENGTH, 0], speed, 0, self.RIGHT_DIR, random.randint(1, 3), follow_dist)
        elif self.direction == self.UP_DIR:
            car = Car([0, -self.INTERSECTION_LENGTH], speed, 0, self.UP_DIR, random.randint(1, 3), follow_dist)
        elif self.direction == self.DOWN_DIR:
            car = Car([0, self.INTERSECTION_LENGTH], speed, 0, self.DOWN_DIR, random.randint(1, 3), follow_dist)

        return car