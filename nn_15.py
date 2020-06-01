from tensorflow import keras
import numpy as np 
from game_15 import Game_15
import pandas as pd 

###############################################
#
# A module for creating a neural network model 
# and datasets for its teaching
#
###############################################

def create_data_sets(sets=1000, iterations = 20):
    # Returns two numpy arrays of game board states and corresponding moves 
    # by shuffling tiles iterations times in sets iterations
    game = Game_15()
    X, Y = np.empty((0, 16), dtype='int32'), np.empty((0, 16), dtype='int32')
    for set in range(sets):
        game.new_game()
        x, y = game.shuffle(iterations, verbose=False)
        for i, item in enumerate(y):
            temp = np.zeros((4, 4), dtype='int32')
            temp[item] = 1
            y[i] = np.reshape(temp, (16))
        for i, item in enumerate(x):
            x[i] = np.reshape(item, (16))
        print(type(x))
        X = np.append(X, x, axis=0)
        Y = np.append(Y, y, axis=0)
    return X, Y

def Model(double=False):
    # Implements a TensorFlow Sequential model with a number of Dense layers

    # I was experimenting with one and two hidden layers and two hidden layers gave a better resalt naturally
    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(16, 1)))
    model.add(keras.layers.Dense(512, activation='sigmoid'))
    if double:
        model.add(keras.layers.Dense(512, activation='sigmoid'))
    model.add(keras.layers.Dense(16, activation='softmax'))
    model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
    model.optimizer.lr = 0.1
    return model

if __name__ == '__main__':
    X, y = create_data_sets()
    model = Model(True)
    hist = model.fit(X, y, validation_split=0.1, epochs=200) # Teaching the model
    print(hist.history)
    model.save_weights('weights_double_1000sets_20iter.h5') # Saving weights for further using
