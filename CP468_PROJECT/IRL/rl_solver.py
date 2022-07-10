from hashlib import sha3_224
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
from Game.minimax import findBestMove
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

states = {}  
f = []
label = []
m = []
def find_Q_table(env,reward,gamma):
    # CHECK HASH FUNC JJFJJFJFJKFDJKJKFSJFDJKFSKJDFKDSKJFSDJKJKFSDJKFJDSJJKSDFJK
    Q = {}
    epsilon = 0.15
    alpha = 0.1
    for _ in range(5000):
        env.reset()
        # print("Iteration ",_)
        # env.pretty_print()
        i=0
        while not env.game_over():
            # x moves
            
            # print(i)
            i+=1
            s = deepcopy(env)
            a = policy(env,Q,epsilon)
            if states.get(hash_state(s),None) is None:
                states[hash_state(s)] = 1
            env.place(a,'x')

            # o makes move
            if hash_state(env)  in LOOKUP_TABLE:
                expert_action = LOOKUP_TABLE[hash_state(env)]
            else:
                expert_action = findBestMove(env,'o')
                LOOKUP_TABLE[hash_state(env)] = expert_action
            
            env.place(expert_action,'o')
            s2 = deepcopy(env)
            if Q.get(hash_state(s2),None) is None:
                
                Q[hash_state(s2)] = {(0,0):0,(0,1):0,(0,2):0,(1,0):0,(1,1):0,(1,2):0,(2,0):0,(2,1):0,(2,2):0}
            
            if Q.get(hash_state(s),None) is None:
                
                Q[hash_state(s)] = {(0,0):0,(0,1):0,(0,2):0,(1,0):0,(1,1):0,(1,2):0,(2,0):0,(2,1):0,(2,2):0}
            
            
            
            else:
                # print("not bad")
                states[hash_state(s)]+=1
            
            
            r = reward(s2)
            if not env.game_over():
                a2 = policy(env,Q,0)
                # print(a2,Q.get(hash_state(s2)))
                Q[hash_state(s)][a] = Q[hash_state(s)][a] + alpha*(r+gamma*Q[hash_state(s2)][a2]- Q[hash_state(s)][a])
                
            else:
                # if vame is over and o was the last one to move update x
                f.append(_)

                label.append(env.who_won()=='default')
                m.append(sum(label)/(_ + 1))
                Q[hash_state(s)][a] += alpha*(r - Q[hash_state(s)][a])

    return Q    

# def reward(s):
#     # if(s.game_over()):
#     #     s.pretty_print()
#     # print(s.evaluate())
#     return s.evaluate()

def rl_solver(board,reward):
    b = Board(10,0)
    Q = find_Q_table(b,reward,0.9)
    return policy(board,Q,0)

# trajectories = generate_trajectories(p)


# def matrix_to_symbols(b):

#     for i in range(len(b)):
#         row = []
#         for j in range(len(b)):
#             if b[i][j] == 1:
#                 row.append('x')
#             elif b[i][j] == 2:
#                 row.append('o')
#             else:
#                 row.append('_')
#         print(row)

# plt.plot(f,m)
# plt.show()
# for episode in trajectories:
#     for b in episode:
#         k = Board(10,0)
#         k._matrix = b[0]

#         matrix_to_symbols(b[0])
#         # print(h(b[0]))
#         # print(b[0])
#         print(hash_state(k),states.get(hash_state(k)),b[1],Q.get(hash_state(k)))
#         print()
#     print('----------------')
# print(states)
