import utils
import numpy as np


AVG_ACCELERATION = 0.001

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

    # assumption: car will break when it sees 

    def __init__(self, pos, speed, acceleration, direction, action, follow_dist):
        self.pos = pos # (x,y)
        self.speed = speed # bounded gaussian
        self.dir = direction # up down left right
        self.action = action # straight left, right, stop
        self.follow_dist = follow_dist # uniform dist
        self.acceleration = acceleration
        self.stopped = False

    def updatePosition(self, cars, lights):
        # find closest car in 'front' going same direction or nearest light
        light_closest_bool = False # true if the light is the closest in the front
        min_dist = float('inf')
        for c in cars:
            if c.dir == self.dir:
                cand = float('inf')
                if self.dir == self.LEFT_DIR and self.pos[0] > c.pos[0]:
                    cand = self.pos[0] - c.pos[0]
                elif self.dir == self.UP_DIR and self.pos[1] < c.pos[1]:
                    cand = c.pos[1] - self.pos[1]
                elif self.dir == self.RIGHT_DIR and self.pos[0] < c.pos[0]:
                    cand = c.pos[0] - self.pos[0]
                elif self.dir == self.DOWN_DIR  and self.pos[1] > c.pos[1]:
                    cand = self.pos[1] - c.pos[1]
                min_dist = min(min_dist, cand)

        # if direction car is going has a red light for that direction OR left turn + cross traffic
        if (lights.state[self.dir] == 1) or \
            (lights.state[self.dir] == 0 and lights.state[(self.dir + 2) % lights.NUM_LIGHTS] == 0 and self.action == self.LEFT_TURN):
            light_dist = max(abs(self.pos[0]), abs(self.pos[1]))
            if light_dist < min_dist:
                light_closest_bool = True
                min_dist = light_dist # how far to the light
        # green light
        

        # if min_dist < float('inf'):
        #     self.acceleration = ((self.speed)**2) / (2 * min_dist)
        #     if min_dist < self.follow_dist:
        #         self.stopped = True
        #         self.speed = 0
        # else:
        #     self.acceleration += AVG_ACCELERATION
        #     self.stopped = False
        # if self.dir == self.LEFT_DIR:
            # print('yuh', self.pos[0])
            # print(min_dist)
        if min_dist < self.follow_dist:
            self.speed = 0
            self.stopped = True
        else:
            # if self.dir == self.LEFT_DIR:
                # print('crossing')
            self.speed = 30 / 3600
            self.stopped = False
        if self.dir == self.LEFT_DIR:
            # self.pos = (currX - self.speed, currY)
            self.pos[0] -= self.speed
        elif self.dir == self.UP_DIR:
            self.pos[1] += self.speed
        elif self.dir == self.RIGHT_DIR:
            self.pos[0] += self.speed
        elif self.dir == self.DOWN_DIR:
            self.pos[1] -= self.speed

    def print(self):
        print(f"pos: {car.pos}, dir: {car.dir}, v: {car.speed}, stopped: {car.stopped}")
        


