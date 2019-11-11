import car
import trafficlight
import utils
import cargenerate 

'''
global vars 
'''
TOTAL_TIME = 1000 # in seconds 
CAR_PROB - 0.8 # prob of a car appearing at any given time step 

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

'''
initialize stuff
'''
all_cars = [] #keeps track of all cars in world
left_cars = []
right_cars = []
top_cars = []
bottom_cars = []
lights = trafficlights() 
left_car_gen = cargenerate(RIGHT_DIR, CAR_PROB)
right_car_gen = cargenerate(LEFT_DIR, CAR_PROB)
up_car_gen = cargenerate(DOWN_DIR, CAR_PROB)
down_car_gen = cargenerate(UP_DIR, CAR_PROB) 

for i in range(TOTAL_TIME):
	#do stuff
	#keep track of closest car to light at all times 
	


