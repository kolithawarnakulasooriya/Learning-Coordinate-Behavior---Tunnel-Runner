import random
import math

OPPONENT_DIRECTION_UP = 1
OPPONENT_DIRECTION_DOWN = 0
WALL_TOP = 40
WALL_BOTTOM = 60

STARTING_X_POS = 10
ENDING_X_POS = 90
STARTING_Y_POS = lambda x: int(x/2)

PRE_COND_STAY_AND_GO = 0
PRE_COND_JUMP_AND_GO = 1

MAX_ENERGY = 10

STATEGY = lambda x: PRE_COND_JUMP_AND_GO if random.uniform(0,1) > x else PRE_COND_STAY_AND_GO
INITIAL_STRATEGY_BOUNDARY = 0.5

"""
The correlation (the Pearson product-moment correlation coefficient) between positive feedback and the status of the behavior is
defined as This gives a statistical measure of the degree to which the status of the behavior (active or not active) is
correlated with positive feedback happening or not.
"""
def calculate_PPA(j, k, l, m):
    d = math.sqrt((m+l)*(m+k)*(j+k)*(j+l))
    if d ==0:
        return 0
    return (j*m - l*k) / d

"""
The reliability of a behavior is defined as (where index P stands for positive feedback and index N stands for negative feedback) The reliability of a behavior ranges from 0 to 1. When
the value is close to 1, the behavior is considered very reliable (i.e. the feedback is very consistent: the probability of receiving feedback is either close to 0 or 
to 1). 
"""
def calculate_reliability(p):
    r1 = p.positive.j+p.positive.l
    r2 = p.negetive.j+p.negetive.l
    if r1==0 or r2==0:
        return 0
    return min([max([p.positive.j/r1, p.positive.l/r1]), max([p.negetive.j/r1, p.negetive.l/r1])])