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
        intersection.step(action)
    return r

# driver for qtable
def qdriver():
    epochs = int(1e3)
    intersection = env.Environment()
    # suffixes = ['1', '2', '3', '4', '5', 'many_iter']
    res = {}
    # for s in suffixes:
    fname = 'mcts_qtable.pkl'
    qt = pickle.load(open(fname, 'rb'))
    intersection.loadQTable(qt)
    start = time.time()
    rewards = []
    for i in range(epochs):
        if (i + 1) % 100 == 0:
            print('iteration', i + 1)
            print(f'time passed: {time.time() - start} seconds')
            print(f'time left: {(time.time() - start) * (epochs / (i + 1) - 1)} seconds')
            # print(len(intersection.QTable))
        rewards.append(simulate(intersection))
    res = sum(rewards) / len(rewards)
    print(res)
    out = open('mcts_results.pkl', 'wb')
    pickle.dump(res, out)
    out.close()


def main():
    qdriver()

if __name__ == "__main__":
    main()