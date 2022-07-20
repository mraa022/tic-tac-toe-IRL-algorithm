from Game.game import Board
from Game.minimax import *
from Game.global_vars import *
import random
import numpy as np
board = Board(10,0)
from copy import deepcopy
def hash_state(state):
    '''
    -------------------------------------------------------------
    hashes the state of the board into a String. so for example if the board was [[1,0,0] then it would hash it to "100000111".
                                                                                 [0,0,0]
                                                                                 [1,1,1]]    
    -------------------------------------------------------------
    parameters:
        state: a Board object that denotes the current state of the board (Board)
    returns:
        result: a string hash of the Board state (Str)
    '''
    matrix = [str(int(x)) for x in state._matrix.flatten()]
    return ''.join(matrix)

def generate_trajectories(phi=findBestMove,player_o_strategy=findBestMove):
    '''
    -------------------------------------------------------------
    given a policy, returns a list of lists where each sublist is an episode that contains the states X has seen and the actions it took
    in them using the given policy. 'O' follows the minimax algorithm
    -------------------------------------------------------------
    parameters:
        phi: the policy of X. X follows the miniMax algorithm by default (lambda function)
    returns:
        trajectories: list of lists where each list is an episode of the game. where each episode contains
        actions state (board object as state) pairs (List of Lists, ea )
    '''
    trajectory = []
    states = {}
    
    for i in [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]:
        curr_episode = []
        # expert move
        best_move = i
        
        state = board
        action = best_move
        curr_episode.append((deepcopy(state._matrix),action))
        x = best_move[0]
        y = best_move[1]
        
        board.place((x,y),'x')
        
        # opnent move
        if hash_state(board) not in states:
            best_move = player_o_strategy(board,'o')
            states[hash_state(board)] = best_move 
        else:
            best_move = states[hash_state(board)]
        
        x = best_move[0]
        y = best_move[1]
       
        board.place((x,y),'o')
        i = 0
        while  not board.game_over():
            # print(i)
            i+=1
            # expert move
            best_move = phi(board,'x')
            
            state = board
            action = best_move
            curr_episode.append((deepcopy(state._matrix),action))
            x = best_move[0]
            y = best_move[1]
            board.place((x,y),'x')
            
            # opnent move
            best_move = player_o_strategy(board,'o')
            x = best_move[0]
            y = best_move[1]
            board.place((x,y),'o')
        trajectory.append(curr_episode)
        board.reset()
    return trajectory
