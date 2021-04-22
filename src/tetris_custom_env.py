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
        self.board = [[0 for y in range(self.col)] for x in range(self.row)]
        self.piece = self.spawn_shape()
        self.game_over = False
        self.score = 0
        self.rows_removed = 0

         # Actions we can take: left, right, up, down
        self.action_space = Discrete(4)
    
    def step(self, action):
        # preform action
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

        reward = self.rows_removed
        self.rows_removed = 0

        info = {}

        # return state, reward, game over, info
        return self.merge(self.board, self.piece), reward, self.game_over, info

    def render(self):
        pass

    def reset(self):
        self.board = [[0 for y in range(self.col)] for x in range(self.row)]
        self.piece = self.spawn_shape()
        self.game_over = False
        self.score = 0
        # reward -= 50


    def move_left(self):
        if self.piece.x > 0:
            temp = self.piece
            temp.x -= 1
            if self.is_valid_position(temp):
                self.piece.x -= 1
    
    def move_right(self):
        if self.piece.x < 9:
            temp = self.piece
            temp.x += 1
            if self.is_valid_position(temp):
                self.piece.x += 1

    def move_down(self):
        temp = self.piece
        temp.y += 1
        if self.is_valid_position(temp):
            self.piece.y += 1
        else:
            # collision! lock piece in place, check for complete rows, spawn a new shape, then check if game is over
            self.score += 1
            self.board = self.merge(self.board, self.piece)
            self.fix_rows()
            self.piece = self.spawn_shape()
            self.check_lost()

    def rotate(self):
        temp = self.piece
        temp.rotate()
        if self.is_valid_position(temp):
            self.piece.rotate()

    def is_valid_position(self, shape):
        merged = self.merge(self.board, shape)
        for y in range(self.row):
            for x in range(self.col):
                if merged[y][x] > 1:
                    return False
        return True

    def merge(self, board, shape):
        x_offset, y_offset = shape.get_offsets()
        # x_offset = len(shape.shape[shape.rotation][0])
        # y_offset = len(shape.shape[shape.rotation])
        new_board = board
        for i in range(self.row):
            for j in range(self.col):
                if j in range(shape.x, shape.x+x_offset) and i in range(shape.y, shape.y+y_offset):
                    new_board[i][j] += shape.shape[shape.rotation][i-shape.y][j-shape.x]
        return new_board
    
    def fix_rows(self):
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
        #remove row at index and shift above rows down
        self.rows_removed += 1

        board = self.board
        while index >= 0:
            row = []
            for j in range(len(self.row)):
                row.append(board[index-1][j])
            board[i] = row
            index -= 1
        board[0] = [0 for x in range(self.col)]
        self.score += 10
        return board
    
    def check_lost(self):
        #check if collision happens at the top row when a new piece spawns
        top_row = self.board[0]
        check = self.is_valid_position(self.piece)
        if check == False and (1 or 2 in top_row):
            self.game_over = True
            # self.reset()
        #     return True
        # else:
        #     return False

    def spawn_shape(self):
        shapes = [self.S, self.Z, self.I, self.O, self.J, self.L, self.T]
        letter = random.choice(shapes)
        return Piece(4, 0, letter)