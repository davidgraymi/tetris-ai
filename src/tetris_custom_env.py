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
        self.board = [[0 for x in range(self.col)] for y in range(self.row)]
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
            pass
            #rotate

    def render(self):
        pass

    def reset(self):
        pass

    def move_left(self):
        self.piece.x -= 1
        if not self.is_valid_position():
            self.piece.x += 1
    
    def move_right(self):
        self.piece.x += 1
        if not self.is_valid_position():
            self.piece.x -= 1

    def move_down(self):
        self.piece.y += 1
        # check for collision

    def is_valid_position(self):
        # check if the piece is in a valid position on the board
        pass
    
    def check_lost(self):
        top_row = self.board[0]
        for square in top_row:
            if square == 1:
                return True
        return False

    def spawn_shape(self):
        shapes = [self.S, self.Z, self.I, self.O, self.J, self.L, self.T]
        return Piece(4, 0, random.choice(shapes))