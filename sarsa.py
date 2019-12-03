import utils
import numpy as np
import env
import time
import multiprocessing
import pickle


def sarsa(intersection):
    timesteps = 1000
    alpha = 0.05
    gamma = 0.9
    action = intersection.chooseAction(intersection.currState)
    for i in range(timesteps):
        r = intersection.reward(intersection.currState, action)
        prevAction = action
        action = intersection.chooseAction(intersection.currState)
        intersection.step()
        intersection.QTable[(intersection.prevState, prevAction)] = (intersection.QTable.get((intersection.prevState, prevAction), 0) * (1 - alpha)
                                                                  + alpha * (r + gamma * intersection.QTable.get((intersection.currState, action), 0)))

def driver():
    epochs = int(1.26e7)
    intersection = env.Environment()
    start = time.time()
    for i in range(epochs):
        if i % 100000 == 0:
            print(i)
            print(f'time passed: {time.time() - start} seconds')
            print(len(intersection.QTable))
        sarsa(intersection)
        intersection.reset()

    f = open('qtable.pkl', 'wb')
    pickle.dump(intersection.QTable, f)
    f.close()

def main():
    driver()
if __name__ == "__main__":
    main()