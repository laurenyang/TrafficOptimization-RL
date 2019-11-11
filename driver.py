import car
import trafficlight
import utils
import cargenerate 

'''
global vars 
'''
TOTAL_TIME = 1000 #in seconds 

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
car_list = [] #keeps track of all cars in world
lights = trafficlights() 
left_car_gen = cargenerate(LEFT_DIR)
right_car_gen = cargenerate(RIGHT_DIR)
up_car_gen = cargenerate(UP_DIR)
down_car_gen = cargenerate(DOWN_DIR) 

for i in range(TOTAL_TIME):
	#do stuff



