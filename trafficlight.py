class TrafficLight:
	def __init__(self, state):
		# state is a list [left light, top light, right light, bottom light] in this order
		self.state = state
		self.lastUpdated = [0, 0, 0, 0] # last timestep that light was updated

	def print(self): 
		print("Traffic Light State: " + str(self.state))

	def changeState(self, newState, t):
		for i in range(len(self.state)):
			if newState[i] != self.state[i]:
				self.lastUpdated[i] = t
		self.state = newState

	def flipState(self, t):
		newState = [v ^ 1 for v in self.state]
		self.changeState(newState, t)