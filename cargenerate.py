import utils
import car
import numpy as np
import random
import scipy.stats

class CarGenerator:
    # speed limit in mph
    MAX_SPEED = 25

    # distance in miles
    INTERSECTION_LENGTH = 0.25

    # directions
    LEFT_DIR = 0
    UP_DIR = 1
    RIGHT_DIR = 2
    DOWN_DIR = 3

    def __init__(self, direction, p):
        # direction
        self.direction = direction
        self.p = p
        self.next_time = 0
        _next_time_car()

    def _next_time_car(self):
        self.next_time += np.random.geometric(self.p)

        # truncated normal from 15 to 40 mph
        speed = scipy.stats.truncnorm.rvs(-10 / 2.5, 15/2.5, loc=25, scale=2.5, size=1)[0]

        # may not use this
        follow_dist = 20 / 5280

        if self.direction == LEFT_DIR:
            self.next_car = Car([INTERSECTION_LENGTH, 0], speed, LEFT_DIR, random.randint(1, 3), follow_dist)
        elif self.direction == RIGHT_DIR:
            self.next_car = Car([-INTERSECTION_LENGTH, 0], speed, RIGHT_DIR, random.randint(1, 3), follow_dist)
        elif self.direction == UP_DIR:
            self.next_car = Car([0, INTERSECTION_LENGTH], speed, UP_DIR, random.randint(1, 3), follow_dist)
        elif self.direction == DOWN_DIR:
            self.next_car = Car([0, -INTERSECTION_LENGTH], speed, DOWN_DIR, random.randint(1, 3), follow_dist)

    def gen_car(self, t):
        if t < self.next_time:
            return None
        else:
            self.next_time = t
            print(self.next_car)
            ret_car = self.next_car
            _next_time_car()
            print(ret_car)
            return ret_car