import random
from piece import Piece
# from gym import Env
# from gym.spaces import Discrete, Box
import numpy as np
import cv2
from PIL import Image


class TetrisEnv:

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

    COLORS = {
        0: (255, 255, 255),
        1: (247, 64, 99),
        2: (0, 167, 247),
        3: (0, 167, 247),
    }

    def __init__(self, render=False):

        self.renderer = render
        self.shapes = [TetrisEnv.S, TetrisEnv.Z, TetrisEnv.I, TetrisEnv.O, TetrisEnv.J, TetrisEnv.L, TetrisEnv.T]
        self.col = 10
        self.row = 20
        self.board = np.zeros((self.row, self.col))
        # self.board = [[0 for x in range(self.col)] for y in range(self.row)]
        self.current_piece = self.spawn_shape()
        self.next_piece = self.spawn_shape()

        self.block_placed = 0
        self.rows_removed = 0
        self.score = 0
        self.game_over = False
        
         # Actions we can take: left, right, up, down
        self.action_space = 4
        # self.action_space = Discrete(4)
        # low = np.zeros((self.row, self.col))
        # high = np.ones((self.row, self.col))
        # high = np.array([4, 20, 100, 150, 20, self.col, self.row])
        # low = np.zeros(7)
        # high = np.array([4, 10, 40, 150])
        # low = np.zeros(4)
        # high = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 20])
        # low = np.zeros(self.col + 1)
        # self.observation_space = Box(low, high, dtype=np.int)
    
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
        
        # after a move left, move right, or rotation move down again if possible
        if action != 2:
            self.move_down()

        if self.renderer:
            self.render()

        info = {}

        game_state = self.get_game_state()

        reward = self.get_reward()
        self.score += reward

        # return state, reward, game over, info
        return game_state, reward, self.game_over, info

    def render(self):
        # Renders the current board

        img = [TetrisEnv.COLORS[p] for row in self.merge(self.board, self.current_piece) for p in row]
        img = np.array(img).reshape(self.row, self.col, 3).astype(np.uint8)
        img = img[..., ::-1] # Convert RRG to BGR (used by cv2)
        img = Image.fromarray(img, 'RGB')
        img = img.resize((self.col * 25, self.row * 25))
        img = np.array(img)
        cv2.putText(img, str(self.score), (22, 22), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        cv2.imshow('image', np.array(img))
        cv2.waitKey(1)

    def reset(self):
        #Reset

        # self.board = [[0 for x in range(self.col)] for y in range(self.row)]
        self.board = np.zeros((self.row, self.col))
        self.current_piece = self.spawn_shape()
        self.next_piece = self.spawn_shape()
        self.block_placed = 0
        self.rows_removed = 0
        self.score = 0
        self.game_over = False
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
            self.check_lost()
            self.current_piece = self.next_piece
            self.next_piece = self.spawn_shape()

    def rotate(self):
        #Rotate

        temp = Piece(self.current_piece.x, self.current_piece.y, self.current_piece.shape, self.current_piece.index, self.current_piece.rotation)
        temp.rotate_clockwise()
        if self.is_valid_position(temp):
            self.current_piece.rotate_clockwise()

    def is_valid_position(self, shape):
        #Checks if the position of the current piece is valid

        x_offset, y_offset = shape.get_offsets()
        lower_edge = shape.y + y_offset
        left_edge = shape.x
        right_edge = shape.x + x_offset

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
                if j in range(shape.x, shape.x+x_offset+1) and i in range(shape.y, shape.y+y_offset+1):
                    new_board[i][j] += shape.shape[shape.rotation][i-shape.y][j-shape.x]
        return new_board
    
    # def fix_rows(self):
    #     # Checks if a complete row exists

    #     for i in range(self.row):
    #         row_count = 0
    #         for j in range(self.col):
    #             if self.board[i][j] == 1:
    #                 row_count += 1
    #             else:
    #                 break

    #             if row_count == 9:
    #                 self.board = self.remove(i)

    def fix_rows(self):
        # Checks if a complete row exists

        for i in range(self.row):
            if 0 not in self.board[i]:
                self.remove(i)

    def remove(self, index):
        #Removes row at index and shifts above rows down

        self.rows_removed += 1
        while index >= 0:
            row = np.copy(self.board[index-1])
            self.board[index] = row
            index -= 1
        self.board[0] = np.zeros(self.col)

    # def remove(self, index):
    #     #Removes row at index and shifts above rows down

    #     self.rows_removed += 1
    #     board = np.copy(self.board)
    #     while index >= 0:
    #         row = np.copy(board[index-1])
    #         board[index] = row
    #         index -= 1
    #     board[0] = np.zeros(self.col)
    #     return board
    
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

    def get_action_space(self):
        return self.action_space

    # def get_bumpiness(self):

    #     bumpiness = 0
    #     for i in range(self.col-1):
    #         for j in range(self.row):
    #             if self.board[j,i] >= 1:
    #                 height_row_1 = self.row - j
    #                 break
    #             height_row_1 = 0
    #         for j in range(self.row):
    #             if self.board[j,i+1] >= 1:
    #                 height_row_2 = self.row - j
    #                 break
    #             height_row_2 = 0
    #         difference = abs(height_row_1 - height_row_2)
    #         # print(height_row_1, "-", height_row_2, "=", difference)
    #         bumpiness += difference
    #     return bumpiness

    def _bumpiness(self):
        '''Sum of the differences of heights between pair of columns'''
        total_bumpiness = 0
        max_bumpiness = 0
        min_ys = []

        for col in zip(*self.board):
            i = 0
            while i < self.row and col[i] != 1:
                i += 1
            min_ys.append(i)
        
        for i in range(len(min_ys) - 1):
            bumpiness = abs(min_ys[i] - min_ys[i+1])
            max_bumpiness = max(bumpiness, max_bumpiness)
            total_bumpiness += abs(min_ys[i] - min_ys[i+1])

        return total_bumpiness, max_bumpiness
            
    # def get_total_height(self):

    #     total_height = 0
    #     for i in range(self.col):
    #         for j in range(self.row):
    #             if self.board[j,i] >= 1:
    #                 height = self.row - j
    #                 break
    #             height = 0
    #         total_height += height
    #     return total_height

    def _height(self):
        '''Sum and maximum height of the board'''
        sum_height = 0
        max_height = 0
        min_height = self.col

        for col in zip(*self.board):
            i = 0
            while i < self.col and col[i] == 0:
                i += 1
            height = self.col - i
            sum_height += height
            if height > max_height:
                max_height = height
            elif height < min_height:
                min_height = height

        return sum_height, max_height, min_height

    # def _height(self):
    #     '''Sum and maximum height of the board'''
    #     heights = np.zeros(self.col)
    #     for i in range(self.col):
    #         for j in range(self.row):
    #             if self.board[j,i] >= 1:
    #                 height = self.row - j
    #                 break
    #             height = 0
    #         heights[i] = height
    #     return heights

    # def get_current_piece(self):

    #     current_piece = self.current_piece.index + self.current_piece.rotation
    #     current_piece = np.array([current_piece])
    #     return current_piece, self.current_piece.x, self.current_piece.y
    
    # def get_next_piece(self):

    #     next_piece = self.next_piece.index + self.next_piece.rotation
    #     return next_piece

    def _number_of_holes(self):
        # Number of holes in the board (empty square with at least one block above it)

        holes = 0

        for col in zip(*self.board):
            i = 0
            while i < self.row and col[i] != 1:
                i += 1
            holes += len([x for x in col[i+1:] if x == 0])

        return holes

    def get_game_state(self):
        lines = self.rows_removed
        holes = self._number_of_holes()
        # bumpiness = self.get_bumpiness()
        total_bumpiness, max_bumpiness = self._bumpiness()
        # heights = self._height()
        sum_height, max_height, min_height = self._height()
        # current_piece, x, y = self.get_current_piece()
        # next_piece = self.get_next_piece()
        game_state = [lines, holes, total_bumpiness, sum_height]
        # game_state = [lines, holes, total_bumpiness, sum_height, current_piece, x, y]
        # game_state = self.merge(self.board, self.current_piece)
        # game_state = np.concatenate((heights, current_piece), axis=None)
        return game_state

        # try the height of each column and the piece
        # lower the columns range to decrease the size of the Q table