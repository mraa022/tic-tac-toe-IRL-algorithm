import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from IRL.main import *
from Game.generate_trajectories import generate_trajectories
from Game.minimax import findBestMove, findLastBestMove, findRandomBestMove
from IRL.rl_solver import solve_rl
from IRL.rl_solver import policy as found_policy
from Game.game import Board
import numpy as np
import matplotlib.pyplot as plt
import Game
def create_board(num_marix):
    hash_num = {1:'x',2:'o'}
    b = Board(10,0)
    for i in range(len(num_marix)):
        for j in range(len(num_marix)):
            if num_marix[i][j] != 0:
                symbol = hash_num[num_marix[i][j]]
                b.place((i,j),symbol)
    return b
def find_win_rate(policy,o_strategy=findBestMove):
    trajectories = generate_trajectories(policy,o_strategy)
    total = 0
    # count the number of games they were in a draw and return that
    for episode in trajectories:
        
        last_board_matrix = episode[-1][0]
        last_board = create_board(last_board_matrix)
        last_board.pretty_print()
        open_slots = last_board.possible_actions()
        if len(open_slots) ==1:
            for slot in open_slots:
                last_board.place(slot,'o') 
                if last_board.evaluate() ==0:
                    total+=1
                last_board.undo_move(slot)
    return total/9

# w,policy = recover_r(phi,0.9,0.2,0.1,max_margin_episodes=100,rl_episodes=30000)
w = np.array([-0.03844113,  0.00841021, -0.00450324 , 0.02462958 , 0.04166667 ,-0.00547929,
  0.03925703 , 0.03118429, -0.02431718]) # gotten after above line is uncommented
reward = lambda s:np.matmul(w,s._matrix.flatten())


# ############################# Analysis and agent for when the RL agent is trained in the same environment the reward was recovered in
player_o_strategy = findBestMove
episodes,win_rate,policy = solve_rl(Board(10,0),reward,0.9,50000,0.2,0.1,return_training_loss=True,verbose=True,player_o_strategy=player_o_strategy)
plt.title("Win rate of the model")
plt.xlabel('episode number')
plt.ylabel('win rate')
plt.plot(episodes,win_rate)
plt.show()
b = Board(10,0)
while True:
    
    bot_action  = policy(b,'x')
    b.place(bot_action,'x')
    b.pretty_print()
    user = input("ENTER ROW COL: ").split(',')
    row,col = int(user[0]),int(user[1])
    b.place((row,col),'o')
    if b.game_over():
        b.reset()



# ############################# Analysis for when the RL agent is asked to adapt in an env where the minimax player O picks the last action
# ############################# if multiple actions have same minimax value
# player_o_strategy = findLastBestMove
# episodes,win_rate,policy = solve_rl(Board(10,0),reward,0.9,50000,0.2,0.1,return_training_loss=True,verbose=True,player_o_strategy=player_o_strategy)
# plt.title("Win rate of the model")
# plt.xlabel('episode number')
# plt.ylabel('win rate')
# plt.plot(episodes,win_rate)
# plt.show()
# b = Board(10,0)
# while True:
    
#     bot_action  = policy(b,'x')
#     b.place(bot_action,'x')
#     b.pretty_print()
#     user = input("ENTER ROW COL: ").split(',')
#     row,col = int(user[0]),int(user[1])
#     b.place((row,col),'o')
#     if b.game_over():
#         b.reset()



# ############################# Analysis for when the RL agent is asked to adapt in an env where the minimax player O picks random action
# ############################# if multiple actions have same minimax value
# player_o_strategy = findRandomBestMove
# episodes,win_rate,policy = solve_rl(Board(10,0),reward,0.9,50000,0.2,0.1,return_training_loss=True,verbose=True,player_o_strategy=player_o_strategy)
# plt.title("Win rate of the model")
# plt.xlabel('episode number')
# plt.ylabel('win rate')
# plt.plot(episodes,win_rate)
# plt.show()
# b = Board(10,0)
# while True:
    
#     bot_action  = policy(b,'x')
#     b.place(bot_action,'x')
#     b.pretty_print()
#     user = input("ENTER ROW COL: ").split(',')
#     row,col = int(user[0]),int(user[1])
#     b.place((row,col),'o')
#     if b.game_over():
#         b.reset()


