import utils
import numpy as np
import env
import multiprocessing
import pickle
import time

# hyperparameters: gamma, c, d, epochs

def selectAction(intersection, d, epochs):
    T = set()
    N = {}
    start = time.time()
    for i in range(epochs):
        if (i + 1) % 100 == 0:
            print('epoch number: ', i + 1)
            print(f'time passed: {time.time() - start} seconds')
            print(f'time left: {(time.time() - start) * (epochs / (i + 1) - 1)} seconds')            
        simulate(intersection, d, T, N)
        intersection.reset()
    return intersection.bestAction(intersection.currState)

def MCTSBestAction(s, intersection, N):
    c = 0.05
    largestQ = float('-inf')
    stateVisits = sum(N[s].values())
    currActionList = []
    for a in intersection.ACTIONS:
        currKey = (s, a)
        currQ =  c * np.sqrt(np.log(stateVisits) / N[s][a])
        if currKey in intersection.QTable:
            currQ += intersection.QTable[currKey]
        if currQ > largestQ: 
            currActionList = [a]
        elif currQ == largestQ: 
            currActionList.append(a)
    action = random.choice(currActionList)

def simulate(intersection, d, T, N):
    gamma = 0.9
    if d == 0:
        return 0
    if intersection.currState not in T:
        T.add(intersection.currState)
        N[intersection.currState] = {}
        for a in intersection.ACTIONS:
            N[intersection.currState][a] = 1
        return rollout(intersection, d)
    else:
        s = intersection.currState
        a = intersection.bestAction(s)
        intersection.step(a)
        q = intersection.reward(s, a) + gamma * simulate(intersection, d - 1, T, N)
        N[s][a] += 1
        intersection.QTable[(s,a)]=intersection.QTable.get((s,a), 0) + (q-intersection.QTable.get((s,a), 0))/N[s][a]
        return q

def rollout(intersection, d):
    if d == 0:
        return 0
    action = intersection.ACTIONS[np.random.randint(0, len(intersection.ACTIONS))]
    intersection.step(action)
    return intersection.reward(intersection.currState, action) + rollout(intersection, d - 1)

def driver():
    d = 100
    epochs = int(2e5)
    intersection = env.Environment()
    selectAction(intersection, d, epochs)

    f = open('mcts_qtable.pkl', 'wb')
    pickle.dump(intersection.QTable, f)
    f.close()


def main():
    driver()
if __name__ == "__main__":
    main()