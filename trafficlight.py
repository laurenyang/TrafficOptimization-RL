class TrafficLight:
	def __init__(self, state):
		# state is a list [left light, top light, right light, bottom light] in this order
		self.state = state
		self.lastUpdated = [0, 0, 0, 0] # last timestep that light was updated

	def print(self): 
		print("Traffic Light State: " + str(self.state))

	def changeState(self, newState):
		self.state = newState