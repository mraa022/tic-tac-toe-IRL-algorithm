from hashlib import sha3_224
from platform import win32_ver
from pyexpat import features
from re import S
import sys
import os
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import matplotlib.pyplot as plt
from Game.game import Board
from copy import deepcopy
from Game.generate_trajectories import generate_trajectories
from Game.minimax import *
ACTION_SPACE = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
import numpy as np
import random
def policy(board,Q,epsilon):
    state = board
    p = np.random.random()
    possible_actions = board.possible_actions()
   
    if p<epsilon:
        return random.choice(possible_actions) 
    if Q.get(hash_state(state),None) is None:
        Q[hash_state(state)] = {(0,0):0,(0,1):0,(0,2):0,(1,0):0,(1,1):0,(1,2):0,(2,0):0,(2,1):0,(2,2):0}
    
    best_val = float('-inf')
    best_action = possible_actions[0]
    for action in ACTION_SPACE:
        action_val = Q[hash_state(state)][action]
        if action_val>best_val and board.is_empty(action):
            best_val  = action_val 
            best_action = action 
    return best_action

LOOKUP_TABLE = {}

def hash_state(state):
    matrix = [str(int(x)) for x in state._matrix.flatten()]
    return ''.join(matrix)

def solve_rl(env,reward,gamma,num_episodes,epsilon,alpha,return_training_loss=False,verbose=False,player_o_strategy=findBestMove):
    '''
    paramaters:
        env: the environment (Object)
        reward: the reward function, takes in as input the state and outputs the reward value (lambda function)
        gamma: the discount factor (float)
        num_episodes: the number of episodes you run before terminating  (Int)
        epsilon: the probability of exploring instead of exploiting (float)
        alpha: the learning rate
    '''
    Q = {}  # the Q table
    episode,win_rate,label = [],[],[]
    for _ in range(num_episodes):
        env.reset()
        if verbose:
            print("Iteration ",_)
        while not env.game_over():
            s = deepcopy(env)
            a = policy(env,Q,epsilon)
            env.place(a,'x')
            # dont alwasy call minimax for O since its very expensive, store the states in a table and only call minimax if 
            # you havent seen the state you are in before
            if hash_state(env)  in LOOKUP_TABLE:
                expert_action = LOOKUP_TABLE[hash_state(env)]
            else:
                expert_action = player_o_strategy(env,'o')
                LOOKUP_TABLE[hash_state(env)] = expert_action
            env.place(expert_action,'o')
            s2 = deepcopy(env)
            # uses lazy evaluation to fill in the Q table with states 
            if Q.get(hash_state(s2),None) is None:
                Q[hash_state(s2)] = {(0,0):0,(0,1):0,(0,2):0,(1,0):0,(1,1):0,(1,2):0,(2,0):0,(2,1):0,(2,2):0}
            if Q.get(hash_state(s),None) is None:      
                Q[hash_state(s)] = {(0,0):0,(0,1):0,(0,2):0,(1,0):0,(1,1):0,(1,2):0,(2,0):0,(2,1):0,(2,2):0}
            r = reward(s2)
            # updates the Q value for that state
            if not env.game_over():
                a2 = policy(env,Q,0)
                Q[hash_state(s)][a] = Q[hash_state(s)][a] + alpha*(r+gamma*Q[hash_state(s2)][a2]- Q[hash_state(s)][a])      
            else:
                Q[hash_state(s)][a] += alpha*(r - Q[hash_state(s)][a])
                episode.append(_)
                label.append(env.who_won()=='default')
                win_rate.append(sum(label)/(_ + 1))

    recovered_policy = lambda state,symbol:policy(state,Q,epsilon=0)
    
    return recovered_policy  if not return_training_loss else (episode,win_rate,recovered_policy) 
