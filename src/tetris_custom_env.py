import random
from piece import Piece
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np


class TetrisEnv(Env):
    def __init__(self):

        S = [
            
            [[0,1,1],
              [1,1,0]],

             [[1,0],
              [1,1],
              [0,1]]
              
            ]

        Z = [

            [[1,1,0],
             [0,1,1]],

            [[0,1],
             [1,1],
             [1,0]]

            ]

        I = [
            
            [[1,1,1,1]],

            [[1],
             [1],
             [1],
             [1],]
            
            ]

        O = [
            
            [[1,1],
             [1,1]],

            [[1,1],
             [1,1]]
            
            ]

        J = [
            
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

        L = [
            
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

        T = [
            
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

        self.shapes = [S, Z, I, O, J, L, T]

        self.block_placed = 0
        self.rows_removed = 0

        self.col = 10
        self.row = 20
        self.board = np.zeros((self.row, self.col))
        # self.board = [[0 for x in range(self.col)] for y in range(self.row)]
        self.current_piece = self.spawn_shape()
        self.next_piece = self.spawn_shape()
        self.game_over = False
        
         # Actions we can take: left, right, up, down
        self.action_space = Discrete(4)
        self.observation_space = Box(low=0, high=201, shape=(1,6), dtype=np.int)
        # self.observation_space = Box(np.array(self.board[0][0]), np.array(self.board[-1][-1]), dtype=np.int)
    
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

        info = {}

        game_state = self.get_game_state()

        reward = self.get_reward()

        # merge = self.merge(self.board, self.current_piece)
        # self.render(merge)

        # return state, reward, game over, info
        return game_state, reward, self.game_over, info

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
        self.current_piece = self.spawn_shape()
        self.next_piece = self.spawn_shape()
        self.game_over = False
        self.block_placed = 0
        self.rows_removed = 0
        return self.get_game_state()


    def move_left(self):
        #Move left

        self.current_piece.x -= 1
        if not self.is_valid_position(self.current_piece):
            self.current_piece.x += 1
    
    def move_right(self):
        #Move right

        self.current_piece.x += 1
        if not self.is_valid_position(self.current_piece):
            self.current_piece.x -= 1

    def move_down(self):
        #Move down

        self.current_piece.y += 1
        if not self.is_valid_position(self.current_piece):
            # collision! lock piece in place, check for complete rows, spawn a new shape, then check if game is over
            self.current_piece.y -= 1
            self.board = self.merge(self.board, self.current_piece)
            self.block_placed += 1
            self.fix_rows()
            self.current_piece = self.next_piece
            self.next_piece = self.spawn_shape()
            self.check_lost()

    def rotate(self):
        #Rotate

        temp = Piece(self.current_piece.x, self.current_piece.y, self.current_piece.shape, self.current_piece.rotation)
        temp.rotate_clockwise()
        if self.is_valid_position(temp):
            self.current_piece.rotate_clockwise()

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

        self.rows_removed += 1
        board = np.copy(self.board)
        while index >= 0:
            row = np.copy(board[index-1])
            board[index] = row
            index -= 1
        board[0] = np.zeros(self.col)
        return board
    
    def check_lost(self):
        #Checks if the concrete pieces have reaches the top of the board

        top_row = np.copy(self.board[0])
        if max(top_row) >= 1:
            self.game_over = True

    def spawn_shape(self):
        #Spawns a new shape at the top of the board
        
        i = len(self.shapes) - 1
        index = random.randint(0,i)
        letter = self.shapes[index]
        # letter = random.choice(self.shapes)
        return Piece(4, 0, letter, index)

    def get_reward(self):
        # reward function

        reward = self.block_placed + (self.rows_removed**2 * self.col)
        if self.game_over:
            reward -= 1
        self.block_placed = 0
        self.rows_removed = 0
        return reward

    def get_bumpiness(self):
        bumpiness = 0
        for i in range(self.col-1):
            for j in range(self.row):
                if self.board[j,i] >= 1:
                    height_row_1 = self.row - j
                    break
                height_row_1 = 0
            for j in range(self.row):
                if self.board[j,i+1] >= 1:
                    height_row_2 = self.row - j
                    break
                height_row_2 = 0
            difference = abs(height_row_1 - height_row_2)
            # print(height_row_1, "-", height_row_2, "=", difference)
            bumpiness += difference
        return bumpiness
            
    def get_total_height(self):
        total_height = 0
        for i in range(self.col):
            for j in range(self.row):
                if self.board[j,i] >= 1:
                    height = self.row - j
                    break
                height = 0
            total_height += height
        return total_height

    def get_holes(self):
        holes = 0
        for i in range(self.row):
            for j in range(self.col):
                if i == 0:
                    break
                if self.board[i,j] == 0:
                    if j == 9:
                        if i == 19:
                            # bottom right corner
                            if self.board[i-1,j] == 1 and self.board[i,j-1] == 1 and self.board[i-1,j-1] == 1:
                                holes += 1
                        else:
                            # right side
                            if self.board[i-1,j] == 1 and self.board[i,j-1] == 1 and self.board[i-1,j-1] == 1 and self.board[i+1,j] == 1 and self.board[i+1,j-1] == 1:
                                holes += 1
                    elif j == 0:
                        if i == 19:
                            # bottom left corner
                            if self.board[i-1,j] == 1 and self.board[i,j+1] == 1 and self.board[i-1,j+1] == 1:
                                holes += 1
                        else:
                            # left side
                            if self.board[i-1,j] == 1 and self.board[i,j+1] == 1 and self.board[i-1,j+1] == 1 and self.board[i+1,j] == 1 and self.board[i+1,j+1] == 1:
                                holes += 1
                    else:
                        if i == 19:
                            # bottom
                            if self.board[i-1,j] == 1 and self.board[i,j+1] == 1 and self.board[i-1,j+1] == 1 and self.board[i,j-1] == 1 and self.board[i-1,j-1] == 1:
                                holes +=1
                        else:
                            # everything else
                            if self.board[i-1,j] == 1 and self.board[i,j-1] == 1 and self.board[i-1,j-1] == 1 and self.board[i+1,j] == 1 and self.board[i,j+1] == 1 and self.board[i+1,j+1] == 1 and self.board[i-1,j+1] == 1 and self.board[i+1,j-1] == 1:
                                holes +=1
        return holes

    def get_current_piece(self):
        current_piece = self.current_piece.index + self.current_piece.rotation
        return current_piece
    
    def get_next_piece(self):
        next_piece = self.next_piece.index + self.next_piece.rotation
        return next_piece

    def get_game_state(self):
        game_state = [self.rows_removed, self.get_holes(), self.get_bumpiness(), self.get_total_height(), self.get_current_piece(), self.get_next_piece()]
        return game_state