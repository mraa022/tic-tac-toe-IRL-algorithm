from Game.global_vars import *
def minimax(board, depth, isMax) :
    
   
    score = board.evaluate()

    if (score == REWARDS['x'] or score==REWARDS['o']) :
        return score

    if (board.is_moves_left() == False) :
        return REWARDS['default']
 
    # If this maximizer's move
    if (isMax) :  
        
        best = -1000
 
        # Traverse all cells
        for i in range(SIZE) :        
            for j in range(SIZE) :
              
                # Check if cell is empty
                if board.is_empty((i,j)) :
                 
                    # Make the move
                    board.place((i,j),'x')
 
                    # Call minimax recursively and choose
                    # the maximum value
                    best = max( best, minimax(board,
                                              depth + 1,
                                              not isMax) )
 
                    # Undo the move
                    board.undo_move((i,j))
        return best
 
    # If this minimizer's move
    else :
        best = 1000
 
        # Traverse all cells
        for i in range(SIZE) :        
            for j in range(SIZE) :
              
                # Check if cell is empty
                if board.is_empty((i,j)) :
                 
                    # Make the move
                    board.place((i,j),'o')
 
                    # Call minimax recursively and choose
                    # the minimum value
                    best = min(best, minimax(board, depth + 1, not isMax))
 
                    # Undo the move
                    board.undo_move((i,j))
        return best
 
# This will return the best possible move for the player
def findBestMove(board,player) :
    
    isMax = IS_MAX[player]
   
    bestVal = float('-inf') if isMax else float('inf')
    
    bestMove = (0, 0)
 
    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for i in range(SIZE) :    
        for j in range(SIZE) :
         
            # Check if cell is empty
            if board.is_empty((i,j)):
             
                # Make the move
                board.place((i,j),player)
 
                # compute evaluation function for this
                # move.
                moveVal = minimax(board, 0, not isMax)
                # print((i,j),moveVal)
                # Undo the move
                board.undo_move((i,j))

                if (moveVal > bestVal) and isMax :   
                    
                    bestMove = (i, j)
                    bestVal = moveVal
                elif (moveVal<bestVal) and not isMax:
                    bestMove = (i,j)
                    bestVal = moveVal
 
    return bestMove
