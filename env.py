import cargenerate
import car
import trafficlight
import utils

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
    self.QTable = {} # (s, a) -> Q-value
    self.seenTuples = set()

    def __init__(self):
        self.reset()

    def step(self):
        # based on car gen + curr cars, update everything
        # choose action - see how like Q(s, a, s') works
            
        # prune cars past the intersection
        self.left_cars, self.right_cars, self.up_cars, self.down_cars, self.all_cars = utils.pruneCars(self.left_cars, self.right_cars, self.up_cars, self.down_cars)
        
        # update positions in reverse queue order
        for car in self.all_cars[::-1]:
            car.updatePosition(self.all_cars, self.lights)

        # generate all cars 
        # left gen generates rightwards going cars
        generated_left_car = self.right_car_gen.gen_car(self.timestep)
        generated_right_car = self.left_car_gen.gen_car(self.timestep)
        
        generated_up_car = self.bottom_car_gen.gen_car(self.timestep)
        generated_down_car = self.top_car_gen.gen_car(self.timestep)

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


    def writeState(self, all_cars, lights):
        pass

    def reward(self, state, action):
        # should take the state and then tell us 
        pass

    def render(self):
        pass

    def reset(self):
        # lists of cars
        self.all_cars = [] #keeps track of all cars in world
        self.left_cars = []
        self.right_cars = []
        self.up_cars = []
        self.down_cars = []
        self.lights = trafficlight.TrafficLight([1, 0, 1, 0]) 
        self.left_car_gen = cargenerate.CarGenerator(self.RIGHT_DIR, self.CAR_PROB)
        self.right_car_gen = cargenerate.CarGenerator(self.LEFT_DIR, self.CAR_PROB)
        self.top_car_gen = cargenerate.CarGenerator(self.DOWN_DIR, self.CAR_PROB)
        self.bottom_car_gen = cargenerate.CarGenerator(self.UP_DIR, self.CAR_PROB)

        self.timestep = 0

        self.prevState = None
        self.currState = None
    
