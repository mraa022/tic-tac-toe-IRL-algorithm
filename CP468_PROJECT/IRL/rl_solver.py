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
    epsilon = 0.1
    alpha = 0.1
    for _ in range(50000):
        env.reset()
        print("Iteration ",_)
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

def reward(s):
    # w = np.array([-0.23552458,  0.10318106,  0.25092175,  0.15571041,  0.23992299,  0.16506025,
#   0.03693527, -0.00483777, -0.00431269])
    w = np.array([-0.01502647, -0.02514172,  0.04525434, -0.02511753,  0.0527855,  -0.04476556,
  0.02843316,  0.00810395, -0.02671182])
    # if(s.game_over()):
    #     s.pretty_print()
    # print(s.evaluate())
    return np.matmul(w,s._matrix.flatten())
# Q = find_Q_table(Board(10,0))
# p = lambda s: policy(Board(10,0),Q,0)
# def rl_solver(board,reward):
#     b = Board(10,0)
#     Q = find_Q_table(b,reward,0.9)
#     return policy(board,Q,0)

# trajectories = generate_trajectories(p)


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
q_table = find_Q_table(Board(10,0),reward,0.9)
plt.plot(f,m)
plt.show()
p = lambda s,symbol:policy(s,q_table,0)
# trajectories = generate_trajectories(p)
# for episode in trajectories:
#     for b in episode:
#         k = Board(10,0)
#         k._matrix = b[0]

#         matrix_to_symbols(b[0])
#         # print(h(b[0]))
#         # print(b[0])
#         # print(hash_state(k),states.get(hash_state(k)),b[1],Q.get(hash_state(k)))
#         print()
#     print('----------------')
# # print(states)
# print(q_table)

b = Board(10,0)
while True:
    
    bot_action  = p(b,'x')
    b.place(bot_action,'x')
    b.pretty_print()
    user = input("ENTER ROW COL: ").split(',')
    row,col = int(user[0]),int(user[1])
    b.place((row,col),'o')
    if b.game_over():
        b.reset()