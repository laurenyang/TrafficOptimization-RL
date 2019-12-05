import utils
import numpy as np
import env
import time
import multiprocessing
import pickle
import random

def randomSimulate(intersection, updateTime=None):
    timesteps = 1000
    action = random.choice(intersection.ACTIONS)
    r = 0
    for i in range(timesteps):
        if updateTime is not None:
            if i % updateTime != 0:
                continue
        r += intersection.reward(intersection.currState, action)
        action = random.choice(intersection.ACTIONS)
        intersection.step(action)
    return r

# driver for random
def rdriver():
    changeIntervals = [1, 2, 3, 5, 10, 15, 20]
    intersection = env.Environment()
    for c in changeIntervals:
        epochs = int(1e3)
        res = {}
        start = time.time()
        rewards = []
        for i in range(epochs):
            if i % 100 == 0:
                print('iteration', i, c)
                print(f'time passed: {time.time() - start} seconds')

            rewards.append(randomSimulate(intersection, c))
        res = sum(rewards) / len(rewards)
        print(res)
    out = open('random_results.pkl', 'wb')
    pickle.dump(res, out)
    out.close()


def main():
    rdriver()

if __name__ == "__main__":
    main()