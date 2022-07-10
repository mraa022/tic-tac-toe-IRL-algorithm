import sys
import os
import numpy as np
from copy import deepcopy
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Game.generate_trajectories import generate_trajectories
from Game.minimax import findBestMove
from IRL.rl_solver import find_Q_table
from IRL.rl_solver import policy as found_policy
from Game.game import Board
import Game
def phi(state):
    if type(state)==Game.game.Board:
        return state._matrix.flatten()
    else: # sometimes state is an actual list (happens in the recover_r function)
        return state.flatten() 
    # except:
    #     # print(state)
    #     return state 

def feature_expectations(trajectories,phi,gamma):
    mu = np.zeros(shape=(9,))
    for trajectory in trajectories:
        for t,state in enumerate(trajectory):
            result = phi(state[0])*(gamma**2)
            mu += phi(state[0])*(gamma**2)
    return mu/len(trajectories)

def recover_r(phi,gamma):
    b = Board(10,0)
    epsilon = 0.01
    gamma = 0.9

    i = 0
    trajectories = generate_trajectories()
    mu_e = feature_expectations(trajectories,phi,gamma)
    pi_o = lambda state,symbol: random.choice(state.possible_actions())
    mu_o = feature_expectations(generate_trajectories(pi_o),phi,gamma)
    policies = [pi_o]
    none_expert_feature_expectations = [mu_o]
    mu_bars = []
    i+=1
    for i in range(1,101):
        if i==1:
            mu_bar_o = deepcopy(mu_o)
            # mu_bars.append(np.zeros(9,))
            mu_bars.append(mu_bar_o)
            w = mu_e - mu_o
        else:
            # mu_bar_prev = mu_bars[-1]
            mu_bar_prev_prev = mu_bars[i-2]
            # print(none_expert_feature_expectations,' f ')
            # print(mu_bars)
            # print()
            mu_prev = none_expert_feature_expectations[i-1]
            # print(mu_e,mu_bar_prev,mu_bar_prev_prev,mu_prev)
            # mu_bar_prev = mu_bar_prev_prev + (((mu_prev-mu_bar_prev_prev).T @ (mu_e-mu_bar_prev_prev))/((mu_prev-mu_bar_prev_prev).T @ (mu_prev-mu_bar_prev_prev)))*(mu_prev-mu_bar_prev_prev)

            # k = ((mu_prev-mu_bar_prev_prev).T @ (mu_e-mu_bar_prev_prev))/((mu_prev-mu_bar_prev_prev).T @ (mu_prev-mu_bar_prev_prev))
            top_half = (mu_prev -mu_bar_prev_prev).T @ (mu_e-mu_bar_prev_prev)
            bottom_half = (mu_prev -mu_bar_prev_prev).T @ (mu_prev-mu_bar_prev_prev)
            mu_bar_prev = mu_bar_prev_prev  + (top_half/bottom_half)*(mu_prev-mu_bar_prev_prev)
               
            w = mu_e - mu_bar_prev
            mu_bars.append(mu_bar_prev)
        reward_function = lambda s: np.matmul(w,phi(s))
        # print(w)
        Q_table = find_Q_table(Board(10,0),reward_function,gamma)
        new_policy = new_policy = lambda s,symbol:found_policy(s,deepcopy(Q_table),epsilon) 


        policies.append(new_policy)
        
        none_expert_feature_expectations.append(feature_expectations(generate_trajectories(new_policy),phi,gamma))
            
        t = np.linalg.norm(mu_e-mu_bars[-1])
        if t<0.5:
            break
        print(t)
    return w,policies[-1]
# def policy(state,symbol):
#     possible_choices = []
#     for x in 
w,policy  = recover_r(phi,0.9)

trajectories = generate_trajectories(policy)


def matrix_to_symbols(b):

    for i in range(len(b)):
        row = []
        for j in range(len(b)):
            if b[i][j] == 1:
                row.append('x')
            elif b[i][j] == 2:
                row.append('o')
            else:
                row.append('_')
        print(row)

# plt.plot(f,m)
# plt.show()
for episode in trajectories:
    for b in episode:
        k = Board(10,0)
        k._matrix = b[0]

        matrix_to_symbols(b[0])
        # print(h(b[0]))
        # print(b[0])
        print()
    print('----------------')
# print(states)
