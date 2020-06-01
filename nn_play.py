from nn_15 import Model
from nn_15_conv import ModelConv
from game_15 import Game_15
import numpy as np 
import pygame as pg 
from game_15_board import play_machine

def test(model, ran, iteration, conv=False):
    # Running a neural network to play game with a range of shuffle iterations
    # ran must be a tuple (minimum shuffle iterations, maximum shuffle iterations + 1)
    # iterations are a number of iterations in each shuffles number
    # returns a dict of received results
    game =  Game_15()
    result = {}
    for r in range(ran[0], ran[1]):
        success = 0
        for i in range(iteration):
            game.new_game()
            game.shuffle(r)
            for j in range(20):
                if game.win:
                    success = success + 1
                    break
                X = game.field
                if conv:
                    X = np.reshape(game.field, (1, 4, 4, 1))
                else:
                    X = np.reshape(game.field, (1, 16))
                y = np.argmax(model.predict(X), axis=-1) 
                move = (int(int(y)//4), int(int(y)%4))
                game.move(move)
        result.update({r: '{0} out of {1}'.format(success, iteration)})
    return result

if __name__ == '__main__':

    # An example of NN playing visualization

    model = Model()
    model.load_weights('weights_5000sets_30iter.h5')
    
    model_double = Model(True)
    model_double.load_weights('weights_double_1000sets_20iter.h5')

    game =  Game_15()
    pg.init()
    play_machine(game, model_double, 6, 20)