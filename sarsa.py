import utils
import numpy as np
import env
import time
import multiprocessing
import pickle


def sarsa(intersection):
    timesteps = 1000
    alpha = 0.1
    gamma = 0.85
    action = intersection.chooseAction(intersection.currState) # at
    for _ in range(timesteps):
        
        intersection.step(action)
        r = intersection.reward(intersection.currState, action)

        prevAction = action
        nextAction = intersection.chooseAction(intersection.currState) # next steps action, at+1
        
        intersection.QTable[(intersection.prevState, prevAction)] = (intersection.QTable.get((intersection.prevState, prevAction), 0) * (1 - alpha)
                                                                  + alpha * (r + gamma * intersection.QTable.get((intersection.currState, nextAction), 0)))
        action = nextAction

def driver():
    epochs = int(2e5)
    intersection = env.Environment()
    fname = '/dfs/scratch0/tigs/traffic/qtable_tiger_small_alpha1_gamma85.pkl'
    start = time.time()
    for i in range(epochs):
        if i % 1000 == 0:
            print(i)
            print(f'time passed: {time.time() - start} seconds')
            print(len(intersection.QTable))
            f = open(fname, 'wb')
            pickle.dump(intersection.QTable, f)
            f.close()

        sarsa(intersection)
        intersection.reset()
    f = open(fname, 'wb')
    pickle.dump(intersection.QTable, f)
    f.close()



def main():
    driver()
if __name__ == "__main__":
    main()
