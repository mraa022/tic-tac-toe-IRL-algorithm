import sys
import os
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Game.generate_trajectories import generate_trajectories
from IRL.rl_solver import solve_rl
from IRL.rl_solver import policy as found_policy
from Game.game import Board
import Game
def phi(state):
    if type(state)==Game.game.Board:
        return state._matrix.flatten()
    else: # sometimes state is an actual list (happens in the recover_r function)
        return state.flatten() 

def feature_expectations(trajectories,phi,gamma):
    mu = np.zeros(shape=(9,))
    for trajectory in trajectories:
        for t,state in enumerate(trajectory):
            # result = phi(state[0])*(gamma**2)
            mu += phi(state[0])*(gamma**t)
    return mu/len(trajectories)
episode_num = []

time_took = []
def recover_r(phi,gamma,epsilon,alpha,max_margin_episodes,rl_episodes):
    '''
    paramater:
        phi: the feature extractor phi (lambda function that outputs vector given state object)
        gamma: the discount factor (float)
        epsilon: the probability of taking random action and exploring instead of exploiting
        alpha: the learning rate the forwarld RL algorithm will use (float)
        max_margin_episodes: the number of episodes the max margin algorithm will run for (int)
        rl_episodes: the number of episodes the forlward RL algorithm will run for to find the optimal policy under the rewrad function it was given (int)
    '''
    i = 0
    b = Board(10,0)
    trajectories = generate_trajectories() #expert trajectories
    mu_e = feature_expectations(trajectories,phi,gamma)
    pi_o = lambda state,symbol: random.choice(state.possible_actions()) # random policy
    mu_o = feature_expectations(generate_trajectories(pi_o),phi,gamma) # feature expecation of random policy
    policies = [pi_o] # a list of policies
    none_expert_feature_expectations = [mu_o] 
    mu_bars = []
    i+=1
    w = np.zeros((9,))
    while i<max_margin_episodes:
        ## Find w so as to make the optimal policy look better than the current policy by the highest margin
        if i==1:
            mu_bar_o = deepcopy(mu_o)
            mu_bars.append(mu_bar_o)
            w = mu_e - mu_o
        else:
            mu_bar_prev_prev = mu_bars[i-2]
            mu_prev = none_expert_feature_expectations[i-1]
            top_half = (mu_prev -mu_bar_prev_prev).T @ (mu_e-mu_bar_prev_prev)
            bottom_half = (mu_prev -mu_bar_prev_prev).T @ (mu_prev-mu_bar_prev_prev)
            mu_bar_prev = mu_bar_prev_prev  + (top_half/bottom_half)*(mu_prev-mu_bar_prev_prev)
               
            w = mu_e - mu_bar_prev
            mu_bars.append(mu_bar_prev)
        reward_function = lambda s: np.matmul(w,phi(s))
        new_policy =solve_rl(b,reward_function,gamma,rl_episodes,epsilon,alpha)
        policies.append(new_policy)
        none_expert_feature_expectations.append(feature_expectations(generate_trajectories(new_policy),phi,gamma))
        t = np.linalg.norm(mu_e-mu_bars[-1])
        print("Error rate ",t)
        i+=1
    # write the weights in the w.txt file just incase you need them later on
    f = open('w.text','w')
    f.write(str(w))
    f.close()
    return w,policies[-1]
