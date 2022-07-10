import sys
import os
import numpy as np
from keras import Sequential
from keras.layers import Dense
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Game.generate_trajectories import generate_trajectories
from Game.minimax import findBestMove
trajectories = generate_trajectories.generate_trajectories(findBestMove)

CLASSES = {}
for t,action in enumerate([(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]):
    CLASSES[action] = t

def one_hot_encode(action):
    default = [0,0,0,0,0,0,0,0,0]
    default[CLASSES[action]] = 1
    return default
features = []
labels = []
for trajectory in trajectories:
    for state,action in trajectory:
        features.append(state.flatten()) #  
        labels.append(one_hot_encode(action))



features = np.array(features)
labels = np.array(labels)
# print(features)

classifier = Sequential()
#First Hidden Layer
classifier.add(Dense(9, activation='relu', input_dim=9))
#Second  Hidden Layer
classifier.add(Dense(4, activation='relu'))
#Output Layer
classifier.add(Dense(9, activation='softmax'))
print("YO")
classifier.compile(optimizer ='adam',loss='categorical_crossentropy', metrics =['accuracy'])
print("HI")
classifier.fit(features,labels, batch_size=10, epochs=5000)

from Game.game import Board
from Game.minimax import findBestMove

b = Board(10,0)
b.place((0,0),'x')
b.place((1,1),'o')
b.place((1,0),'x')
b.place((0,1),'o')
b._matrix=b._matrix.reshape((1,9)) 
# print(b._matrix.flatten().shape)
# print(features[0],features[0].shape)
print(classifier.predict(b._matrix))