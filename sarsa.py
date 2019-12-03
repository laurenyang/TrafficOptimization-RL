import utils
import numpy as np
import env

def sarsa_lambda():
    # epsilon greedy exploration strategy
    epochs = 10e5
    alpha = 0.05
    gamma = 0.9
    intersection = Environment()
    action = intersection.chooseAction(intersection.currState)
    for _ in range(epochs):
        r = intersection.reward(intersection.currState, action)
        prevAction = action
        action = intersection.chooseAction(intersection.currState)
        intersection.step()
        intersection.QTable[(intersection.prevState, prevAction)] = intersection.QTable[(intersection.prevState, prevAction)] * (1 - alpha) 
                                                                  + alpha * (r + gamma * intersection.QTable[(intersection.currState, action)])
