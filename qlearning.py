import utils
import numpy as np
import env
import time
import multiprocessing
import pickle


def qlearning(intersection):
    timesteps = 1000
    alpha = 0.1
    gamma = 0.8
    
    for _ in range(timesteps):
        action = intersection.chooseAction(intersection.currState)
        intersection.step(action)
        r = intersection.reward(intersection.currState, action)
        intersection.QTable[(intersection.prevState, action)] = (intersection.QTable.get((intersection.prevState, action), 0) * (1 - alpha)
                                                                  + alpha * (r + gamma * intersection.QTable.get((intersection.currState, intersection.bestAction(intersection.currState)), 0)))

def driver():
    epochs = int(2e5)
    intersection = env.Environment()
    start = time.time()
    fname= '/dfs/scratch0/tigs/traffic/qtable_qlearning_alpha1_gamma8.pkl'
    for i in range(epochs):
        if i % 100 == 0:
            print(i)
            print(f'time passed: {time.time() - start} seconds')
            print(f'estimated time to completion: {(time.time() - start) * (epochs / (i + 1) - 1)} seconds')
            print(f'unique states encountered: {len(intersection.QTable)}')
            f = open(fname, 'wb')
            pickle.dump(intersection.QTable, f)
            f.close()

        qlearning(intersection)
        intersection.reset()

    f = open(fname, 'wb')
    pickle.dump(intersection.QTable, f)
    f.close()

def main():
    driver()
if __name__ == "__main__":
    main()
