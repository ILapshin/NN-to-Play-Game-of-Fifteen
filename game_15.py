import numpy as np 

class Game_15:
    #####################################
    #
    # A main class describing game logic fully
    #
    # You should shuffle game board after creating every new game
    #
    #####################################
    def __init__(self):
        self.template = np.array([[i + 1 + j * 4 for i in range(4)] for j in range(4)], dtype='int') # A sample of right positioned tiles
        self.gap = (3, 3) # A parameter that contains the current position of the gap
        self.template[self.gap] = 0
        self.new_game()

    def new_game(self):
        # Created new unshuffled game board
        self.field = np.copy(self.template)
        self.gap = (3, 3)
        self.win = False

    def move(self, cell):
        # Committing a single move
        # Returns True if a move was successfully done and False otherwise
        if cell == tuple(self.gap):
            return False

        if 0 in self.field[cell[0], :]:
            direction = int((cell[1] - self.gap[1]) / abs(self.gap[1] - cell[1]))
            for i in range(self.gap[1], cell[1], direction):
                self.field[cell[0], i] = self.field[cell[0], i + direction]
            self.gap = cell
            self.field[self.gap] = 0
            if np.array_equal(self.field, self.template):
                self.win = True
            return True

        elif 0 in self.field[:, cell[1]]:
            direction = int((cell[0] - self.gap[0]) / abs(self.gap[0] - cell[0]))
            for i in range(self.gap[0], cell[0], direction):
                self.field[i, cell[1]] = self.field[i + direction, cell[1]]
            self.gap = cell
            self.field[self.gap] = 0
            if np.array_equal(self.field, self.template):
                self.win = True
            return True

        else:
            return False

    def shuffle(self, iter, verbose=False):
        # Shuffles the game board iter times by a row and a column alternatively
        # Returns a tuple of two arrays of game board state and a move made to reach that state in every iteration

        X = [] 
        y = []

        is_row = True
        for i in range(iter):
            y.append(self.gap)
            if verbose:        
                print(self.field, '\n')
            if is_row:
                move = False
                while not move:
                    move = self.move((self.gap[0], np.random.randint(4)))
                    is_row = False
            else:
                move = False
                while not move:
                    move = self.move((np.random.randint(4), self.gap[1]))
                    is_row = True
            X.append(np.copy(self.field))
        print(self.field, '\n')
        self.win = False    
        return X, y
     
    def check_win(self):
        # Returns True if current game board state equals the sample 
        if self.win:
            return True
        else:
            return False  

def play(shuf=10):
    # A method for playing via console
    score = shuf
    a = Game_15()
    a.shuffle(shuf)
    while not a.win:
        try:
            x, y = input('enter cell: ').split(' ')
        except Exception as e:
            print(e)    
            continue
        x, y = int(x), int(y)
        try:
            k = a.move((x, y))
        except Exception:
            print('incorrect coordinates')
            continue
        if k:
            print(a.field)
            score = score - 1
            print('Score: {0}'.format(score))
    print('win! Score: {0}'.format(score))
    while True:
        input('press any key')
        break

def random_play(max_iter=100000):
    # I was curious, if it is possible to solve the puzzle performing just random moves
    # It isn't
    a = Game_15()
    a.shuffle(5, verbose=True)
    for i in range(max_iter):
        k = False
        while not k:
            k = a.move((np.random.randint(4), np.random.randint(4)))
        print('iter {0} copleted'.format(i), '\n', a.field)
        if a.win:
            print('finished in {0} iterations'.format(i))
            return


