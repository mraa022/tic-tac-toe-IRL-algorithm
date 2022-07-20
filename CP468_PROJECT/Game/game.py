import numpy as np

ENCODE_SYMBOL = {'x':1,'o':-1,'_':0}

class Board():
    def __init__(self,max_score,default_val):
        self._matrix = np.zeros((3,3))
        self._encode_symbol = {'x':1,'o':2,'_':0}
        self.board = [ [ '_', '_', '_' ],
                        [ '_', '_', '_' ],
                        [ '_', '_', '_' ]]
        self._moves_left = 9
        self._max_score = max_score
        self._min_score = -self._max_score
        self._default = default_val
    def pretty_print(self):
        
        for x in self.board:
            print([y for y in x])
            print()
    def place(self,location,symbol):
        if self._moves_left != 0:
            row = location[0]
            col = location[1]
            

            self.board[row][col] = symbol
            self._matrix[row][col] = self._encode_symbol[symbol]
            self._moves_left-=1
           
    def who_won(self):
        
        for row in range(3):
            
            if self.board[row][0]==self.board[row][1]==self.board[row][2]:
                if self.board[row][0] == 'x':
                    
                    return 'x'
                if self.board[row][0] == 'o':
                    return 'o'
        for col in range(3):

            if self.board[0][col]==self.board[1][col] == self.board[2][col]:
                if self.board[0][col]=='x':
                    return 'x'
                if self.board[0][col]=='o':
                    return 'o'
        if self.board[0][0]==self.board[1][1] == self.board[2][2]:
            if self.board[0][0]=='x':
                return 'x'
            if self.board[0][0]=='o':
                return 'o'

        if self.board[0][2]==self.board[1][1]==self.board[2][0]:
            if self.board[0][2]=='x':
                return 'x'
            if self.board[0][2]=='o':
                return 'o'
       
        return 'default'
    def evaluate(self):
        who_won = self.who_won()
        if who_won == 'default':
            return self._default
        if who_won=='x':
            return self._max_score
        else:
            return self._min_score
    def reset(self):
        self.board = [ [ '_', '_', '_' ],
                        [ '_', '_', '_' ],
                        [ '_', '_', '_' ]]
        self._moves_left = 9
        self._matrix = np.zeros((3,3))
    def is_moves_left(self):
        return self._moves_left != 0
    def is_empty(self,location):
        row = location[0]
        col = location[1]
        return self.board[row][col]=='_'
    def undo_move(self,location):
        i = location[0]
        j = location[1]
        self.board[i][j] = '_'
        self._moves_left+=1
        self._matrix[i][j] = 0
    def game_over(self):
        if self._moves_left == 0:
            return True
        value = self.evaluate()
        return value != self._default
   
    def possible_actions(self):
        result = []
        for i in range(3):
            for j in range(3):
                if self.is_empty((i,j)):
                    result.append((i,j))
        return result