import random
from piece import Piece
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np


class TetrisEnv(Env):
    def __init__(self):

        self.S = [
            
            [[0,1,1],
              [1,1,0]],

             [[1,0],
              [1,1],
              [0,1]]
              
            ]

        self.Z = [

            [[1,1,0],
             [0,1,1]],

            [[0,1],
             [1,1],
             [1,0]]

            ]

        self.I = [
            
            [[1,1,1,1]],

            [[1],
             [1],
             [1],
             [1],]
            
            ]

        self.O = [
            
            [[1,1],
             [1,1]],

            [[1,1],
             [1,1]]
            
            ]

        self.J = [
            
            [[1,0,0],
             [1,1,1]],

            [[1,1],
             [1,0],
             [1,0]],

            [[1,1,1],
             [0,0,1]],

            [[0,1],
             [0,1],
             [1,1]]
            
            ]

        self.L = [
            
            [[0,0,1],
             [1,1,1]],

            [[1,0],
             [1,0],
             [1,1]],

            [[1,1,1],
             [1,0,0]],

            [[1,1],
             [0,1],
             [0,1]]
            
            ]

        self.T = [
            
            [[0,1,0],
             [1,1,1]],

            [[1,0],
             [1,1],
             [1,0]],

            [[1,1,1],
             [0,1,0]],

            [[0,1],
             [1,1],
             [0,1]]
            
            ]

        self.col = 10
        self.row = 20
        self.board = np.zeros((self.row, self.col))
        # self.board = [[0 for x in range(self.col)] for y in range(self.row)]
        self.piece = self.spawn_shape()
        self.game_over = False
        self.score = 0
        
         # Actions we can take: left, right, up, down
        self.action_space = Discrete(4)
        self.observation_space = Box(np.array(self.board[0][0]), np.array(self.board[-1][-1]), dtype=np.int)
    
    def step(self, action):
        #Preform action

        if action == 0:
            self.move_left()
        elif action == 1:
            self.move_right()
        elif action == 2:
            self.move_down()
        elif action == 3:
            self.rotate()
        
        # after a move left, move right, or rotation move down again
        if action != 2:
            self.move_down()

        reward = self.score
        self.score = 0

        info = {}

        merge = self.merge(self.board, self.piece)

        # return state, reward, game over, info
        return merge, reward, self.game_over, info

    def render(self, state):
        #Render

        print("\n")
        for x in range(len(state)):
            print(state[x])
        print("\n")

    def reset(self):
        #Reset

        # self.board = [[0 for x in range(self.col)] for y in range(self.row)]
        self.board = np.zeros((self.row, self.col))
        self.piece = self.spawn_shape()
        self.game_over = False
        self.score = 0
        return self.merge(self.board, self.piece)


    def move_left(self):
        #Move left

        self.piece.x -= 1
        if not self.is_valid_position(self.piece):
            self.piece.x += 1
    
    def move_right(self):
        #Move right

        self.piece.x += 1
        if not self.is_valid_position(self.piece):
            self.piece.x -= 1

    def move_down(self):
        #Move down

        self.piece.y += 1
        if not self.is_valid_position(self.piece):
            # collision! lock piece in place, check for complete rows, spawn a new shape, then check if game is over
            self.piece.y -= 1
            self.score += 1
            self.board = self.merge(self.board, self.piece)
            self.fix_rows()
            self.piece = self.spawn_shape()
            self.check_lost()

    def rotate(self):
        #Rotate

        temp = Piece(self.piece.x, self.piece.y, self.piece.shape, self.piece.rotation)
        temp.rotate_clockwise()
        if self.is_valid_position(temp):
            self.piece.rotate_clockwise()

    def is_valid_position(self, shape):
        #Checks if the position of the current piece is valid

        x_offset, y_offset = shape.get_offsets()
        lower_edge = shape.y + y_offset - 1
        left_edge = shape.x
        right_edge = shape.x + x_offset - 1

        if lower_edge > 19:
            return False
        if left_edge < 0:
            return False
        if right_edge > 9:
            return False
        
        merged = self.merge(self.board, shape)

        for y in range(self.row):
            for x in range(self.col):
                if merged[y][x] > 1:
                    return False
        return True

    def merge(self, board, shape):
        #Merges the board and shape into one array

        x_offset, y_offset = shape.get_offsets()
        new_board = np.copy(board)
        for i in range(self.row):
            for j in range(self.col):
                if j in range(shape.x, shape.x+x_offset) and i in range(shape.y, shape.y+y_offset):
                    new_board[i][j] += shape.shape[shape.rotation][i-shape.y][j-shape.x]
        return new_board
    
    def fix_rows(self):
        # Checks if a complete row exists

        for i in range(self.row):
            row_count = 0
            for j in range(self.col):
                if self.board[i][j] == 1:
                    row_count += 1
                else:
                    break

                if row_count == 9:
                    self.board = self.remove(i)

    def remove(self, index):
        #Removes row at index and shifts above rows down

        self.score += 10

        # print("reomve row:{}".format(index))
        # board = self.board
        board = np.copy(self.board)
        while index >= 0:
            # row = []
            row = np.copy(board[index-1])
            # for j in range(self.row):
            #     row.append(board[index-1][j])
            board[index] = row
            index -= 1
        # board[0] = [0 for x in range(self.col)]
        board[0] = np.zeros(self.col)
        return board
    
    def check_lost(self):
        #Checks if the concrete pieces have reaches the top of the board

        top_row = np.copy(self.board[0])
        if max(top_row) >= 1:
            self.game_over = True

    def spawn_shape(self):
        #Spawns a new shape at the top of the board

        shapes = [self.S, self.Z, self.I, self.O, self.J, self.L, self.T]
        letter = random.choice(shapes)
        return Piece(4, 0, letter)