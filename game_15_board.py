import pygame as pg
from game_15 import Game_15
import time
import numpy as np 
import threading

#################################################
#
# This is a module for creating a visual implementation of Game_15 class using PyGame 
#
# It can be used both to play manually using play_manual() method
# and to show a neural network playing
#
#################################################

class Button:
    # A class for creating a button with some text
    def __init__(self, surf, x, y, width, height, text = ''):
        self.surf = surf
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.draw()

    def draw(self):
        # Draws a button on the game board
        color = (200, 200, 200)
        pg.draw.rect(self.surf, color, (self.x, self.y, self.height, self.width))
        pg.draw.rect(self.surf, (0, 0, 0), (self.x, self.y, self.height, self.width), 2)
        font_obj = pg.font.Font("freesansbold.ttf", 32)
        text_surface = font_obj.render(self.text, True, (0, 0, 0))
        text_rect_obj = text_surface.get_rect()
        text_rect_obj.center = (self.x + self.height // 2, self.y + self.width // 2)
        self.surf.blit(text_surface, text_rect_obj)
        pg.display.update()

    def press(self, pos):
        # Returns True if passed coordinates are within button's borders
        if pos[0] > self.x and pos[1] > self.y and pos[0] < self.x + self.height and pos[1] < self.y + self.width:
            return True
        else:
            return False

class EmptyButton(Button):
    # A utility button for paving the gap
    def __init__(self, surf, x, y, width, height):
        Button.__init__(self, surf, x, y, width, height)

    def draw(self):
        color = (192, 192, 170)
        pg.draw.rect(self.surf, color, (self.x, self.y, self.height, self.width))
        pg.display.update()

def draw_board(field):
    # The main method for drawing a game board
    # Current field state must be passed
    HEIGHT = 520
    WIDTH = 420
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill((192, 192, 170))
    new_game_button = Button(screen, 10, 10, 90, 190, text='New game')
    buttons = []
    for i, row in enumerate(field):
        for j, number in enumerate(row):
            if number != 0:
                buttons.append(Button(screen, 10 + j * 100, 110 + i * 100, 90, 90, text=str(number)))
            else:
                buttons.append(EmptyButton(screen, 10 + j * 100, 110 + i * 100, 90, 90))
    pg.display.update()
    return buttons, new_game_button
    
def play_manual(game, shuf):
    # Allows to play with GUI
    game.shuffle(shuf)
    buttons, new_game_button = draw_board(game.field)
    while True:
        for event in pg.event.get():        
            if event.type == pg.QUIT:
                quit() 
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.press(pg.mouse.get_pos()) and not game.win:
                        if game.move(((button.y - 110) // 100, (button.x - 10) // 100)):
                            draw_board(game.field)
                if new_game_button.press(pg.mouse.get_pos()):
                    game.new_game()
                    game.shuffle(shuf)
                    draw_board(game.field)

def play_machine(game, model, shuf, max_iter):
    # Visualization of a neural network playing the game
    # game should be a Game_15 instance
    # model should be a trained TensorFlow neural network model 
    game.shuffle(shuf)
    buttons, new_game_button = draw_board(game.field)
    counter = shuf
    for i in range(max_iter):
        for event in pg.event.get():        
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if new_game_button.press(pg.mouse.get_pos()):
                    play_machine(game, model, shuf, max_iter)
        
        if not game.win:  
            X = np.reshape(game.field, (1, 16))
            y = np.argmax(model.predict(X), axis=-1) 
            move = (int(int(y)//4), int(int(y)%4))
            game.move(move)
            counter = counter - 1
            time.sleep(1)
            draw_board(game.field)
        else:
            print(counter)
            break
    while True:
        for event in pg.event.get():        
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if new_game_button.press(pg.mouse.get_pos()):
                    play_machine(game, model, shuf, max_iter)

if __name__ == '__main__':
    game = Game_15()
    pg.init() # Pygame must me initialized before running 
    play_manual(game, 5)
