import utils
import numpy as np
import env
import time
import multiprocessing
import pickle
import random

def randomSimulate(intersection, updateTime=None):
    timesteps = 1000
    r = 0
    for i in range(timesteps):
        if updateTime is not None:
            if i % updateTime == 0:
                action = random.choice(intersection.ACTIONS)
        
        intersection.step(action)
        r += intersection.reward(intersection.currState, action)
    return r

# driver for random
def rdriver():
    changeIntervals = list(range(1, 20))
    intersection = env.Environment()
    res = {}
    for c in changeIntervals:
        epochs = int(5e2)
        start = time.time()
        rewards = []
        for i in range(epochs):
            if i % 100 == 0:
                print('iteration', i, c)
                print(f'time passed: {time.time() - start} seconds')

            rewards.append(randomSimulate(intersection, c))
        res[c] = sum(rewards) / len(rewards)
        print(res)
    out = open('random_results.pkl', 'wb')
    pickle.dump(res, out)
    out.close()


def main():
    rdriver()

if __name__ == "__main__":
    main()