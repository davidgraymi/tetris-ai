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

         # Actions we can take: left, right, up, down
        self.action_space = Discrete(4)
    
    def step(self, action):
        if action == 0:
            self.move_left()
        elif action == 1:
            self.move_right()
        elif action == 2:
            self.move_down()
        elif action == 3:
            self.rotate()

    def render(self):
        pass

    def reset(self):
        pass

    def move_left(self):
        if self.piece.x > 0:
            temp = self.piece.x
            temp.x -= 1
            if self.is_valid_position(temp):
                self.piece.x -= 1
    
    def move_right(self):
        if self.piece.x < 9:
            temp = self.piece.x
            temp.x += 1
            if self.is_valid_position(temp):
                self.piece.x += 1

    def move_down(self):
        self.piece.y += 1
        # check for downard collision

    def rotate(self):
        self.piece.rotation += 1
        piece.fix_rotation()
        # fix x and y coordinates in the case that the rotation causes overlapping

    def is_valid_position(self, shape):
        b1 = self.board
        merged = merge(b1, shape)
        for y in range(self.col):
            for x in range(self.row):
                if merged > 1:
                    return False
        return True

    def merge(self, board, shape):
        x_offset, y_offset = shape.get_offsets()
        # x_offset = len(shape.shape[shape.rotation][0])
        # y_offset = len(shape.shape[shape.rotation])
        new_board = [[0 for y in range(self.col)] for x in range(self.row)]
        for i in range(len(shape.shape[shape.rotation])):
            for j in range(len(shape.shape[shape.rotation][0])):
                if j in range(shape.shape.x, shape.shape.x+x_offset) and i in range(shape.shape.y, shape.shape.y+y_offset):
                    new_board[i][j] += 1
        return new_board
    
    def check_lost(self):
        top_row = self.board[0]
        for square in top_row:
            if square == 1:
                return True
        return False

    def spawn_shape(self):
        shapes = [self.S, self.Z, self.I, self.O, self.J, self.L, self.T]
        return Piece(4, 0, random.choice(shapes))