import utils
import numpy as np
import env
import time
import multiprocessing
import pickle
import os

def simulate(intersection):
    timesteps = 1000
    action = intersection.chooseAction(intersection.currState)
    r = 0
    for i in range(timesteps):
        r += intersection.reward(intersection.currState, action)
        action = intersection.bestAction(intersection.currState)
        print('bruh', action,  intersection.currState, intersection.reward(intersection.currState, action))
        if i > 100:
            1/0
        intersection.step(action)
    return r

# driver for qtable
def qdriver():
    epochs = int(1e2)
    intersection = env.Environment()
    import os
    fs = []
    for filename in os.listdir('qpkls/traffic'):
        if filename.endswith(".pkl"): 
            fs.append(filename)
    
    res = {}
    fs = ['qtable_test.pkl']
    for fn in fs:
        fname = f'qpkls/traffic/{fn}'
        fname = fn
        print(fname)
        try:
            qt = pickle.load(open(fname, 'rb'))
        except:
            continue
        intersection.loadQTable(qt)
        start = time.time()
        rewards = []
        for i in range(epochs):
            if i % 100 == 0:
                print('iteration', i, fn)
                print(f'time passed: {time.time() - start} seconds')
                print(len(intersection.QTable))

            rewards.append(simulate(intersection))
        res[fn] = sum(rewards) / len(rewards)
        print(res)
    out = open('sara_results.pkl', 'wb')
    pickle.dump(res, out)
    out.close()


def main():
    qdriver()

if __name__ == "__main__":
    main()