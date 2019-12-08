import utils
import numpy as np
import env
import time
import multiprocessing
import pickle
import random

def heuristicSimulate(intersection, updateTime=None):
    timesteps = 1000
    r = 0
    for i in range(timesteps):
        if updateTime is not None:
            if i % updateTime == 0:
                action = intersection.greedyActionTurn()
        
        intersection.step(action)
        r += intersection.reward(intersection.currState, action)
    return r

# driver for random
def rdriver():
    changeIntervals = list(range(1, 10))
    intersection = env.Environment()
    res = {}
    for c in changeIntervals:
        epochs = int(3e2)
        start = time.time()
        rewards = []
        for i in range(epochs):
            if i % 100 == 0:
                print('iteration', i, c)
                print(f'time passed: {time.time() - start} seconds')

            rewards.append(heuristicSimulate(intersection, c))
        res[c] = sum(rewards) / len(rewards)
        print(res)
    out = open('heuristic_results.pkl', 'wb')
    pickle.dump(res, out)
    out.close()


def main():
    rdriver()

if __name__ == "__main__":
    main()