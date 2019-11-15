import numpy as np

def calculateReward(cars):
    cost = 0
    for c in cars:
        if c.stopped:
            cost -= 1
    return cost

# no longer consider cars that are past 
def pruneCars(left_cars, right_cars, top_cars, bottom_cars):
    new_left = []
    new_right = []
    new_top = []
    new_bottom = []

    for c in left_cars:
        if c.dir != c.LEFT_DIR:
            print("SOMETHING WRONG")
        
        if not (c.dir == c.LEFT_DIR and c.pos[0] < 0):
            new_left.append(c)
    
    for c in right_cars:
        if c.dir != c.RIGHT_DIR:
            print("SOMETHING WRONG")
        
        if not (c.dir == c.RIGHT_DIR and c.pos[0] > 0):
            new_right.append(c)

    for c in top_cars:
        if c.dir != c.UP_DIR:
            print("SOMETHING WRONG")
        
        if not (c.dir == c.UP_DIR and c.pos[1] > 0):
            new_top.append(c)
    
    for c in bottom_cars:
        if c.dir != c.DOWN_DIR:
            print("SOMETHING WRONG")
        
        if not (c.dir == c.DOWN_DIR and c.pos[1] < 0):
            new_bottom.append(c)
        
    
    return new_left, new_right, new_top, new_bottom, new_left + new_right + new_top + new_bottom
