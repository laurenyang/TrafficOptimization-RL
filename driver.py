import car
import trafficlight
import utils
import cargenerate 
import random
import numpy as np
import matplotlib.pyplot as plt

'''
global vars 
'''
TOTAL_TIME = 50 # in seconds 
CAR_PROB = 1 # prob of a car appearing at any given time step 

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

def printCar(car):
	return f"pos: {car.pos}, dir: {car.dir}, v: {car.speed}, stopped: {car.stopped}, action: {car.action}"

def randomFlipBenchmarking():
	'''
	initialize stuff
	'''
	# np.random.seed(0)
	epochs = 1
	switch = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # constant time for when to switch
	avg_costs = []
	switch = [5]
	print('beginning')
	# switchRange = [5, 10, 120]
	for s in switch:
		costs = []
		for _ in range(epochs):
			all_cars = [] #keeps track of all cars in world
			left_cars = []
			right_cars = []
			up_cars = []
			down_cars = []
			lights = trafficlight.TrafficLight([1, 0, 1, 0]) 
			left_car_gen = cargenerate.CarGenerator(RIGHT_DIR, CAR_PROB)
			right_car_gen = cargenerate.CarGenerator(LEFT_DIR, CAR_PROB)
			top_car_gen = cargenerate.CarGenerator(DOWN_DIR, CAR_PROB)
			bottom_car_gen = cargenerate.CarGenerator(UP_DIR, CAR_PROB) 
			cost = 0
			nextSwitchTime = 0
			for i in range(TOTAL_TIME):
				#do stuff
				if i == nextSwitchTime:
					lights.flipLight(i)
					# nextSwitchTime = i + random.randint(1, s)
					nextSwitchTime = i + s
				# if i % s == 0:
				# 	lights.flipLight(i)

				# print('all car', i, len(all_cars))
				# # print(len(left_cars) + len(right_cars) + len(up_cars) + len(down_cars))
				# if len(left_cars) > 0:
				# 	print('left', printCar(left_cars[0]))
				print('left', len(left_cars))
				print(lights.state)
				for _, l in enumerate(left_cars):
					print(printCar(l))
				

				# print('up')
				# for u in up_cars:
				# 	print(printCar(u))

				# print('right')
				# for r in right_cars:
				# 	print(printCar(r))

				# print('down')
				# for d in down_cars:
				# 	print(printCar(d))
				# if len(right_cars) > 0:
				# 	print('right', printCar(right_cars[0]))
				# if len(up_cars) > 0:
				# 	print('up', printCar(up_cars[0]))
				# if len(down_cars) > 0:
				# 	print('down', printCar(down_cars[0]))
				# all_cars = utils.pruneCars(all_cars)
				#update existing cars
				left_cars, right_cars, up_cars, down_cars, all_cars = utils.pruneCars(left_cars, right_cars, up_cars, down_cars)
				all_cars_list = sum(all_cars, [])
				for car in all_cars_list:
					car.updatePosition(all_cars_list, lights)

				#generate all cars 
				# left gen generates rightwards going cars
				generated_left_car = right_car_gen.gen_car(i)
				generated_right_car = left_car_gen.gen_car(i)
				
				generated_up_car = bottom_car_gen.gen_car(i)
				generated_down_car = top_car_gen.gen_car(i)

				if generated_left_car: 
					left_cars.append(generated_left_car)
					all_cars.append(generated_left_car)
				if generated_right_car: 
					right_cars.append(generated_right_car)
					all_cars.append(generated_right_car)
				if generated_up_car: 
					up_cars.append(generated_up_car)
					all_cars.append(generated_up_car)
				if generated_down_car: 
					down_cars.append(generated_down_car)
					all_cars.append(generated_down_car)
				cost += utils.calculateReward(all_cars_list)
			costs.append(cost)
		print(costs)
		# plt.xlabel('Wait time')
		# plt.ylabel('Frequency')
		# plt.title(f'Wait time histogram for random wait time (max {s})')
		# plt.hist(costs, normed=True, bins=50)
		# plt.savefig(f'random{s}.png')
		# plt.close()

	# 	avg_costs.append(np.average(np.array(costs)))
	# print(avg_costs)

	# plt.plot(switch, avg_costs, 'bo--', linewidth=2, markersize=12)
	# plt.show()




def main():
	randomFlipBenchmarking()
	

	

if __name__ == "__main__":
	main()

	






