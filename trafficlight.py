class TrafficLight:
	def __init__(self, state):
		self.state = state

	def print(self): 
		print("Traffic Light State: " + str(self.state))

	def changeState(newState):
		self.state = newState