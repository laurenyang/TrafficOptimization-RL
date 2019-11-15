import car
import trafficlight
import utils
import cargenerate 

'''
global vars 
'''
TOTAL_TIME = 10 # in seconds 
CAR_PROB = 0.10 # prob of a car appearing at any given time step 

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
lights = trafficlight.TrafficLight([1, 1, 0, 0]) 
left_car_gen = cargenerate.CarGenerator(RIGHT_DIR, CAR_PROB)
right_car_gen = cargenerate.CarGenerator(LEFT_DIR, CAR_PROB)
up_car_gen = cargenerate.CarGenerator(DOWN_DIR, CAR_PROB)
down_car_gen = cargenerate.CarGenerator(UP_DIR, CAR_PROB) 

for i in range(TOTAL_TIME):
	#do stuff

	print('all car', i, len(all_cars))
	# all_cars = utils.pruneCars(all_cars)
	#update existing cars
	left_cars, right_cars, top_cars, bottom_cars, all_cars = utils.pruneCars(left_cars, right_cars, top_cars, bottom_cars)
	for car in all_cars:
		car.updatePosition(all_cars, lights)

	#generate all cars 
	# left gen generates rightwards going cars
	generated_left_car = right_car_gen.gen_car(i)
	generated_right_car = left_car_gen.gen_car(i)
	
	generated_up_car = down_car_gen.gen_car(i)
	generated_down_car = up_car_gen.gen_car(i)

	if generated_left_car: 
		left_cars.append(generated_left_car)
		all_cars.append(generated_left_car)
	if generated_right_car: 
		right_cars.append(generated_right_car)
		all_cars.append(generated_right_car)
	if generated_up_car: 
		top_cars.append(generated_up_car)
		all_cars.append(generated_up_car)
	if generated_down_car: 
		bottom_cars.append(generated_down_car)
		all_cars.append(generated_down_car)

	






