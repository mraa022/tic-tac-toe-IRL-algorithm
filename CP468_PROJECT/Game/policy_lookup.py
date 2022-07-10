import sys
import os
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Game.game import Board
from copy import deepcopy
from Game.minimax import findBestMove
ACTION_SPACE = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
import numpy as np
import random



b = Board(10,0)
def hash(s):
    total = 0
    for i in range(s):
        total += (s[i])*(10**i)
    return total


