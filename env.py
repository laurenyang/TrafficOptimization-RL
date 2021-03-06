import cargenerate
import car
import trafficlight
import utils
import random 
import numpy as np
import itertools

# call instance of environment
# environment has a state space, action space
# it would run with rules set forward in utils.updateCars

class Environment:
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

    def __init__(self):
        self.NUM_LIGHTS = 4
        for cand in itertools.product([0,1], repeat = self.NUM_LIGHTS):
            valid = True
            for idx in range(len(cand)):
                if cand[idx] == 0 and cand[(idx + 1) % self.NUM_LIGHTS] == 0:
                    valid = False
            if valid:
                self.ACTIONS.append(cand)
        self.ACTIONS.remove((1, 1, 1, 1))
        self.reset()
        # Q-learning variables
        

    def step(self, action):
        # based on car gen + curr cars, update everything
        # choose action - see how like Q(s, a, s') works
        
        if action is not None:
            self.lights.changeLight(action, self.timestep)

        # prune cars past the intersection
        self.left_cars, self.right_cars, self.up_cars, self.down_cars, self.all_cars = utils.pruneCars(self.left_cars, self.right_cars, self.up_cars, self.down_cars)
        
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
        

    def createInitialState(self):
        numSlices = int(self.INTERSECTION_LENGTH / self.GRID_SIZE) // 4

        left = [0] * numSlices
        right = [0] * numSlices
        up = [0] * numSlices
        down = [0] * numSlices

        lights = [1, 1, 1, 1]

        return (tuple(left), tuple(right), tuple(up), tuple(down), tuple(lights), 0)

    def writeState(self, all_cars, lights):
        # state will be [[left disc], [up disc], [right disc], [bottom disc], lights, numStopped]
        numSlices = int(self.INTERSECTION_LENGTH / self.GRID_SIZE) // 4
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


        return (tuple(left), tuple(right), tuple(up), tuple(down), tuple(lights), utils.numberStopped(all_cars[0] + all_cars[1] + all_cars[2] + all_cars[3]))


    # choose action in sarsa? epsilon-greedy

    def chooseAction(self, s):
        # loop over all possible state-action pairs and loop over all actions take max
        p = np.random.random()
        # for loop over all actions, store best action w best reward
        # look at (s, a) -> Q-value from the QTable, and if (s, a) is not in QTable, assume it is float('-inf')
        # if tie, choose first or random
        if p < self.EPSILON: 
            #explore
            action = self.ACTIONS[np.random.randint(0, len(self.ACTIONS))]
        else: 
            #chose based on reward]
            largestQ = float('-inf')
            #loop over actions instead 
            currActionList = []
            for a in self.ACTIONS:
                currKey = (s, a)
                currQ = float('-inf')
                if currKey in self.QTable:
                    currQ = self.QTable[currKey]
                if currQ > largestQ: 
                    currActionList = [a]
                    largestQ = currQ
                elif currQ == largestQ: 
                    currActionList.append(a)
            action = random.choice(currActionList)
        self.lights.changeLight(action, self.timestep)            
        return action 

    def bestAction(self, s):
        largestQ = float('-inf')
        #loop over actions instead 
        currActionList = []
        for a in self.ACTIONS:
            
            if a == (1, 1, 1, 1):
                continue
            currKey = (s, a)
            currQ = float('-inf')
            if currKey in self.QTable:
                currQ = self.QTable[currKey]
            if currQ > largestQ: 
                currActionList = [a]
                largestQ = currQ
            elif currQ == largestQ: 
                currActionList.append(a)
        action = random.choice(currActionList)
        return action

    def greedyActionNoTurn(self):
        lstopped = utils.numberStopped(self.left_cars)
        rstopped = utils.numberStopped(self.right_cars)
        ustopped = utils.numberStopped(self.up_cars)
        dstopped = utils.numberStopped(self.down_cars)
        mx = max(lstopped, rstopped, ustopped, dstopped)
        if mx == lstopped:
            action = (0, 1, 0, 1)
        elif mx == rstopped:
            action = (0, 1, 0, 1)
        elif mx == ustopped:
            action = (1, 0, 1, 0)
        elif mx == dstopped:
            action = (1, 0, 1, 0)
        return action
    
    def greedyActionTurn(self):
        lstopped = utils.numberStopped(self.left_cars)
        rstopped = utils.numberStopped(self.right_cars)
        ustopped = utils.numberStopped(self.up_cars)
        dstopped = utils.numberStopped(self.down_cars)
        mx = max(lstopped, rstopped, ustopped, dstopped)
        if mx == lstopped:
            action = (0, 1, 1, 1)
        elif mx == rstopped:
            action = (1, 1, 0, 1)
        elif mx == ustopped:
            action = (1, 0, 1, 1)
        elif mx == dstopped:
            action = (1, 1, 1, 0)
        return action

    def reward(self, state, action):
        # should take the state and then tell us 
        _, _, _, _, currLights, numStopped = state

        return -(numStopped + int(tuple(action) != tuple(currLights)) * self.LIGHTCHANGECOST)

    def render(self):
        pass

    def loadQTable(self, qt):
        self.QTable = qt

    def reset(self):
        # lists of cars
        self.all_cars = [] #keeps track of all cars in world
        self.left_cars = []
        self.right_cars = []
        self.up_cars = []
        self.down_cars = []
        self.lights = trafficlight.TrafficLight([1, 1, 1, 1]) 
        self.left_car_gen = cargenerate.CarGenerator(self.RIGHT_DIR, self.CAR_PROB)
        self.right_car_gen = cargenerate.CarGenerator(self.LEFT_DIR, self.CAR_PROB)
        self.top_car_gen = cargenerate.CarGenerator(self.DOWN_DIR, self.CAR_PROB)
        self.bottom_car_gen = cargenerate.CarGenerator(self.UP_DIR, self.CAR_PROB)
        self.INTERSECTION_LENGTH = self.left_car_gen.INTERSECTION_LENGTH
        self.GRID_SIZE = self.left_car_gen.FOLLOW_DIST / 2

        self.timestep = 0

        self.prevState = self.createInitialState()
        self.currState = self.createInitialState()
    
