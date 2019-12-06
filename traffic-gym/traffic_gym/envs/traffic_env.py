import numpy as np
import itertools
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import copy
import random
import scipy.stats

# call instance of environment
# environment has a state space, action space
# it would run with rules set forward in utils.updateCars

class TrafficEnv(gym.Env):
    '''
    global vars 
    '''
    CAR_PROB = 0.1 # prob of a car appearing at any given time step 

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

    # Q-learning variables
    QTable = {} # (s, a) -> Q-value
    seenTuples = set()

    LIGHTCHANGECOST = 1
    EPSILON = .05
    ACTIONS = []

    MAX_CARS = 5

    actionsDict = {
        0: [0, 0, 0, 0],
        2: [ 0, 1, 0, 0],
        1: [1, 0, 0, 0],
        3: [0, 0, 1, 0],
        4: [0, 0, 0, 1],
        5: [0, 1, 0, 1],
        6: [ 1, 0, 1, 0]
        }

    


    def __init__(self):
        # represent state vector as [5] * 4  + [4] + [1]
        self.observation_space = spaces.MultiDiscrete([2] * 24 + [20]) 
        self.action_space = spaces.Discrete(7)

        self.NUM_LIGHTS = 4
        for cand in itertools.product([0,1], repeat = self.NUM_LIGHTS):
            valid = True
            for idx in range(len(cand)):
                if cand[idx] == 0 and cand[(idx + 1) % self.NUM_LIGHTS] == 0:
                    valid = False
            if valid:
                self.ACTIONS.append(cand)
        self.reset()
        # Q-learning variables
        

    def step(self, action):
        # based on car gen + curr cars, update everything
        # choose action - see how like Q(s, a, s') works
        
        if action is not None:
            action = self.actionsDict[action]
            self.lights.changeLight(action, self.timestep)

        # prune cars past the intersection
        self.left_cars, self.right_cars, self.up_cars, self.down_cars, self.all_cars = pruneCars(self.left_cars, self.right_cars, self.up_cars, self.down_cars)
        
        # update positions in reverse queue order
        all_cars_list = sum(self.all_cars, [])
        for car in all_cars_list:
            car.updatePosition(all_cars_list, self.lights)

        # generate all cars 
        # left gen generates rightwards going cars
        generated_left_car = self.right_car_gen.gen_car(self.timestep) if len(self.left_cars) < self.MAX_CARS else None
        generated_right_car = self.left_car_gen.gen_car(self.timestep) if len(self.right_cars) < self.MAX_CARS else None
 
        generated_up_car = self.bottom_car_gen.gen_car(self.timestep) if len(self.up_cars) < self.MAX_CARS else None
        generated_down_car = self.top_car_gen.gen_car(self.timestep) if len(self.down_cars) < self.MAX_CARS else None

        if generated_left_car: 
            self.left_cars.append(generated_left_car)
            self.all_cars.append(generated_left_car)
        if generated_right_car: 
            self.right_cars.append(generated_right_car)
            self.all_cars.append(generated_right_car)
        if generated_up_car: 
            self.up_cars.append(generated_up_car)
            self.all_cars.append(generated_up_car)
        if generated_down_car: 
            self.down_cars.append(generated_down_car)
            self.all_cars.append(generated_down_car)
        
        self.timestep += 1
        self.prevState = self.currState
        self.currState = self.writeState(self.all_cars, self.lights.state)

        return self.currState, self.reward(self.currState, action), False, None

    def createInitialState(self):
        # numSlices = int(self.INTERSECTION_LENGTH / self.GRID_SIZE) // 4
        numSlices = 5

        left = [0] * numSlices
        right = [0] * numSlices
        up = [0] * numSlices
        down = [0] * numSlices

        lights = [1, 1, 1, 1]

        return tuple(left + right + up + down + lights + [0])

    def writeState(self, all_cars, lights):
        # state will be [[left disc], [up disc], [right disc], [bottom disc], lights, numStopped]
        # numSlices = int(self.INTERSECTION_LENGTH / self.GRID_SIZE) // 4
        numSlices = 5
        # leftDiscr = np.linspace(self.INTERSECTION_LENGTH, 0, numSlices)
        # upDiscr = np.linspace(-self.INTERSECTION_LENGTH, 0, numSlices)
        # rightDiscr = np.linspace(-self.INTERSECTION_LENGTH, 0, numSlices)
        # downDiscr = np.linspace(self.INTERSECTION_LENGTH, 0, numSlices)

        left = [0] * numSlices
        right = [0] * numSlices
        up = [0] * numSlices
        down = [0] * numSlices

        # left
        for car in all_cars[0]:
            val = abs(int(car.pos[0] / self.GRID_SIZE))
            if val < numSlices:
                left[val] = 1
        
        # right
        for car in all_cars[1]:
            val = abs(int(car.pos[0] / self.GRID_SIZE))
            if val < numSlices:
                right[val] = 1
        
        # up
        for car in all_cars[2]:
            val = abs(int(car.pos[1] / self.GRID_SIZE))
            if val < numSlices:
                up[val] = 1
        
        # down
        for car in all_cars[3]:
            val = abs(int(car.pos[1] / self.GRID_SIZE))
            if val < numSlices:
                down[val] = 1

        return tuple(left + right + up + down + lights + [numberStopped(all_cars[0] + all_cars[1] + all_cars[2] + all_cars[3])])

    # choose action in sarsa? epsilon-greedy

    def reward(self, state, action):
        # should take the state and then tell us 
        currLights, numStopped = state[-5:-1], state[-1]

        return -(numStopped + int(action != currLights) * self.LIGHTCHANGECOST)

    def render(self):
        pass

    def reset(self):
        # lists of cars
        self.all_cars = [] #keeps track of all cars in world
        self.left_cars = []
        self.right_cars = []
        self.up_cars = []
        self.down_cars = []
        self.lights = TrafficLight([1, 1, 1, 1]) 
        self.left_car_gen = CarGenerator(self.RIGHT_DIR, self.CAR_PROB)
        self.right_car_gen = CarGenerator(self.LEFT_DIR, self.CAR_PROB)
        self.top_car_gen = CarGenerator(self.DOWN_DIR, self.CAR_PROB)
        self.bottom_car_gen = CarGenerator(self.UP_DIR, self.CAR_PROB)
        self.INTERSECTION_LENGTH = self.left_car_gen.INTERSECTION_LENGTH
        self.GRID_SIZE = self.left_car_gen.FOLLOW_DIST / 2

        self.timestep = 0

        self.prevState = self.createInitialState()
        self.currState = self.createInitialState()
        return self.currState

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

class TrafficLight:
	def __init__(self, state):
		# state is a list [left light, up light, right light, bottom light] in this order
		self.state = state
		self.lastUpdated = [0, 0, 0, 0] # last timestep that light was updated


		# defines all possible actions
		self.actionSpace = []

		self.NUM_LIGHTS = 4
		for cand in itertools.product([0,1], repeat = self.NUM_LIGHTS):
			valid = True
			for idx in range(len(cand)):
				if cand[idx] == 0 and cand[(idx + 1) % self.NUM_LIGHTS] == 0:
					valid = False
			if valid:
				self.actionSpace.append(cand)
		# 1 is red

		# state should be [[],[],[],[]]
		# T should be dependent on the car generation at first

	def changeLight(self, newState, t):
		for i in range(len(self.state)):
			if newState[i] != self.state[i]:
				self.lastUpdated[i] = t
		self.state = newState

	def flipLight(self, t):
		newState = [v ^ 1 for v in self.state]
		self.changeLight(newState, t)

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
    FOLLOW_DIST = 132 / 5280

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
        # speed = (scipy.stats.truncnorm.rvs(-10 / 2.5, 15/2.5, loc=25, scale=2.5, size=1)[0]) / 3600

        speed = 30 / 3600

        # may not use this
        


        # cars should not be accelerating
        if self.direction == self.LEFT_DIR:
            car = Car([self.INTERSECTION_LENGTH, 0], speed, 0, self.LEFT_DIR, random.randint(1,3), self.FOLLOW_DIST)
        elif self.direction == self.RIGHT_DIR:
            car = Car([-self.INTERSECTION_LENGTH, 0], speed, 0, self.RIGHT_DIR, random.randint(1,3), self.FOLLOW_DIST)
        elif self.direction == self.UP_DIR:
            car = Car([0, -self.INTERSECTION_LENGTH], speed, 0, self.UP_DIR, random.randint(1,3), self.FOLLOW_DIST)
        elif self.direction == self.DOWN_DIR:
            car = Car([0, self.INTERSECTION_LENGTH], speed, 0, self.DOWN_DIR, random.randint(1,3), self.FOLLOW_DIST)

        return car

### UTILS ############################################

def calculateReward(cars):
    cost = 0
    for c in cars:
        if c.stopped:
            cost -= 1
    return cost

def numberStopped(cars):
    num = 0
    for c in cars:
        if c.stopped:
            num += 1
    return num

# no longer consider cars that are past 
def pruneCars(left_cars, right_cars, top_cars, bottom_cars):
    new_left = []
    new_right = []
    new_top = []
    new_bottom = []

    for c in left_cars:
        if c.dir != c.LEFT_DIR:
            print("SOMETHING WRONG")
        
        if not (c.dir == c.LEFT_DIR and c.pos[0] < 0):
            new_left.append(c)
    
    for c in right_cars:
        if c.dir != c.RIGHT_DIR:
            print("SOMETHING WRONG")
        
        if not (c.dir == c.RIGHT_DIR and c.pos[0] > 0):
            new_right.append(c)

    for c in top_cars:
        if c.dir != c.UP_DIR:
            print("SOMETHING WRONG")
        
        if not (c.dir == c.UP_DIR and c.pos[1] > 0):
            new_top.append(c)
    
    for c in bottom_cars:
        if c.dir != c.DOWN_DIR:
            print("SOMETHING WRONG")
        
        if not (c.dir == c.DOWN_DIR and c.pos[1] < 0):
            new_bottom.append(c)
        
    
    return new_left, new_right, new_top, new_bottom, [new_left, new_right, new_top, new_bottom]