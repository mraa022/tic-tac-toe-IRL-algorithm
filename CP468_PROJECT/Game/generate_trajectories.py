from Game.game import Board
from Game.minimax import *
from Game.global_vars import *
board = Board(10,0)
from copy import deepcopy

def generate_trajectories(phi=findBestMove):
    trajectory = []
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
        best_move = findBestMove(board,'o')
        
        x = best_move[0]
        y = best_move[1]
        board.place((x,y),'o')
        
        while  not board.game_over():
            
            # expert move
            best_move = phi(board,'x')
            
            state = board
            action = best_move
            curr_episode.append((deepcopy(state._matrix),action))
            x = best_move[0]
            y = best_move[1]
            board.place((x,y),'x')
            
            # opnent move
            best_move = findBestMove(board,'o')
            x = best_move[0]
            y = best_move[1]
            board.place((x,y),'o')
        trajectory.append(curr_episode)
        board.reset()
    return trajectory
# trajectories = generate_trajectories()
# for episode in trajectories:
#     for b in episode:
#         b[0].pretty_print()
#         print()
#     print('----------------')
# print(len(trajectories))