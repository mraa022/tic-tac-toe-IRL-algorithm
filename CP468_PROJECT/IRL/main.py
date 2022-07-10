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
    trajectories = generate_trajectories()
    gamma = 0.9

    
    nonexpert_policies = [lambda state,symbol:random.choice([x for x in [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)] if state.is_empty(x)])] # start with random policy
    reward = lambda s:np.matmul(w,phi(s))
    expert_feature_expectations = feature_expectations(trajectories,phi,gamma)

    none_expert_trajectories = generate_trajectories(nonexpert_policies)

    nonexpert_feature_expectations  = none_expert_trajectories # mu_o
    nonexpert_blended_feature_expectations = deepcopy(nonexpert_feature_expectations) # mu_bar_o
    w = expert_feature_expectations - nonexpert_feature_expectations
    # nonexpert_blended_feature_expectations = np.vstack((nonexpert_blended_feature_expectations,np.zeros(shape=(9,))))
    for _ in range(10):
        
        policy = nonexpert_policies[-1]
        trajectories = generate_trajectories(policy)
        nonexpert_feature_expectations = np.vstack((nonexpert_feature_expectations,
                                                        feature_expectations(trajectories,phi,gamma)))
        # Use the projection method to find our current error
        mu_e = expert_feature_expectations
        mu_prev = nonexpert_feature_expectations[-1]

        mu_prev_prev = nonexpert_feature_expectations[-2]
        mu_bar_prev_prev = nonexpert_blended_feature_expectations[-2]
        # print('ffff ',mu_prev_prev)
        # The below finds the orthogonal projection of the expert's
        # feature expectations onto the line through mu_prev and
        # mu_prev_prev
        mu_bar_prev = mu_bar_prev_prev + ((mu_prev - mu_bar_prev_prev.T @ (mu_e-mu_bar_prev_prev))/(mu_prev - mu_bar_prev_prev.T @ (mu_prev-mu_bar_prev_prev)))@(mu_prev-mu_bar_prev_prev)
        # mu_bar_prev = mu_bar_prev_prev \
        #     + (mu_prev - mu_bar_prev_prev).T \
        #         @ (mu_e - mu_bar_prev_prev) \
        #     / (mu_prev - mu_bar_prev_prev).T \
        #         @ (mu_prev - mu_bar_prev_prev) \
        #     * (mu_prev - mu_bar_prev_prev)

        nonexpert_blended_feature_expectations = np.vstack(
            (
                nonexpert_blended_feature_expectations,
                mu_bar_prev
            )
        )

        w = mu_e - mu_bar_prev

        # print(w)
        # Lambda for the current reward estimate
        # print(phi(b).shape,'ffff')
        reward_function = lambda s: np.matmul(w.T, phi(s))
        # reward_function = lambda s: print(phi(s))

        # Check the error of the current hyperplane, and break if we're close
        # to the expert's feature expectations
        t = np.linalg.norm(w)
        print('FFFFFFF ',np.linalg.norm(mu_e-mu_bar_prev))
        if t < epsilon:
            break

        # Compute a new optimal policy using the current reward function
        Q_table = find_Q_table(b,reward_function,gamma)
        new_policy = lambda s,symbol:found_policy(s,deepcopy(Q_table),epsilon)
        nonexpert_policies.append(new_policy)
    return w,nonexpert_policies[-1]
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
