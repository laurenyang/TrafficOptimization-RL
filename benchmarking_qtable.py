import utils
import numpy as np
import env
import time
import multiprocessing
import pickle

def simulate(intersection):
    timesteps = 1000
    action = intersection.chooseAction(intersection.currState)
    r = 0
    for _ in range(timesteps):
        r += intersection.reward(intersection.currState, action)
        action = intersection.bestAction(intersection.currState)
        intersection.step()
    return r

# driver for qtable
def qdriver():
    epochs = int(1e3)
    intersection = env.Environment()
    suffixes = ['1', '2', '3', '4', '5', 'many_iter']
    res = {}
    for s in suffixes:
        fname = f'qpkls/qtable_tiger_small_{s}.pkl'
        qt = pickle.load(open(fname, 'rb'))
        intersection.loadQTable(qt)
        start = time.time()
        rewards = []
        for i in range(epochs):
            if i % 100 == 0:
                print('iteration', i, suffixes)
                print(f'time passed: {time.time() - start} seconds')
                print(len(intersection.QTable))

            rewards.append(simulate(intersection))
        res[s] = sum(rewards) / len(rewards)
    print(res)
    out = open('sara_results.pkl', 'wb')
    pickle.dump(res, out)
    out.close()


def main():
    qdriver()

if __name__ == "__main__":
    main()