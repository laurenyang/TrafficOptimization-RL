import itertools

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
		# [(0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (0, 1, 0, 1), (1, 0, 0, 0), (1, 0, 1, 0)]

		# state should be [[],[],[],[]]
		# T should be dependent on the car generation at first
			

	
		# constraint: [a, b, c, d] consecutive letters cannot be 1 at the same time - cannot update a single
		# light again before 3 seconds
		
		# step 1: -> <- left turn both directions
		# step 2: -> <- straight both directions
		# step 3: ^ ~^ left turn both directions
		# step 4: ^ ~^ left turn both directions


	def print(self): 
		print("Traffic Light State: " + str(self.state))

	def changeLight(self, newState, t):
		for i in range(len(self.state)):
			if newState[i] != self.state[i]:
				self.lastUpdated[i] = t
		self.state = newState

	def flipLight(self, t):
		newState = [v ^ 1 for v in self.state]
		self.changeLight(newState, t)