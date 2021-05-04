import random
from piece import Piece
import numpy as np
import cv2
from PIL import Image
from time import sleep


class Tetris:

    WIDTH = 10
    HEIGHT = 20

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

    SHAPES = [S, Z, I, O, J, L, T]

    COLORS = {
        0: (255, 255, 255),
        1: (247, 64, 99),
        2: (0, 167, 247),
    }


    def __init__(self):
        self.reset()


    # def log(self, board):
    #     print("\n")
    #     for row in board:
    #         print(row)
    #     print("\n")


    def reset(self):
        self.board = np.zeros((Tetris.HEIGHT, Tetris.WIDTH))
        self.game_over = False
        self.next_piece = self.spawn_shape()
        self.round_start()
        self.score = 0
        return self.get_game_state(self.board)

    
    def play(self, x, rotation, render=False, render_delay=None):
        '''Makes a play given a position and a rotation, returning the reward and if the game is over'''
        self.current_piece.x = x
        self.current_piece.rotation = rotation

        # Drop piece until collision
        while not self._check_collision(self.current_piece.shape[self.current_piece.rotation], [self.current_piece.x, self.current_piece.y]):
            if render:
                self.render()
                if render_delay:
                    sleep(render_delay)
            self.current_piece.y += 1
        self.current_piece.y -= 1

        # Update board and calculate score
        self.board = self.merge(self.current_piece)
        lines_cleared, self.board = self._clear_lines(self.board)
        score = 1 + (lines_cleared ** 2) * Tetris.WIDTH
        self.score += score

        # Start new round
        self.round_start()
        if self.game_over:
            score -= 2

        return score, self.game_over

    
    def round_start(self):
        '''Starts a new round (new piece)'''
        
        self.current_piece = self.next_piece
        self.next_piece = self.spawn_shape()

        if self._check_collision(self.current_piece.shape[self.current_piece.rotation], [self.current_piece.x, self.current_piece.y]):
            self.game_over = True

    
    def spawn_shape(self):
        #Spawns a new shape at the top of the board
        
        i = len(Tetris.SHAPES) - 1
        index = random.randint(0,i)
        letter = Tetris.SHAPES[index]
        # letter = random.choice(Tetris.SHAPES)
        return Piece(letter, index)


    def get_game_score(self):
        return self.score


    def merge(self, shape):
        #Merges the board and shape into one array
        board = np.copy(self.board)
        x_offset, y_offset = shape.get_offsets()
        board[shape.y:shape.y+y_offset, shape.x:shape.x+x_offset] += shape.shape[shape.rotation]
        return board


    def _check_collision(self, piece, pos):
        '''Check if there is a collision between the current piece and the board'''

        for j in range(len(piece)):
            for i in range(len(piece[j])):
                piece_block = piece[j][i]
                x = i + pos[0]
                y = j + pos[1]
                if x < 0 or x >= Tetris.WIDTH or y < 0 or y >= Tetris.HEIGHT or (piece_block == self.board[y][x] == 1):
                    return True
        
        return False


    def _clear_lines(self, board):
        '''Clears completed lines in a board'''
        # Check if lines can be cleared
        lines_to_clear = [index for index, row in enumerate(board) if sum(row) == Tetris.WIDTH]
        if lines_to_clear:
            board = [row for index, row in enumerate(board) if index not in lines_to_clear]
            # Add new lines at the top
            for _ in lines_to_clear:
                board.insert(0, [0 for _ in range(Tetris.WIDTH)])
        return len(lines_to_clear), board


    def _number_of_holes(self, board):
        '''Number of holes in the board (empty sqquare with at least one block above it)'''
        holes = 0

        for col in zip(*board):
            i = 0
            while i < Tetris.HEIGHT and col[i] != 1:
                i += 1
            holes += len([x for x in col[i+1:] if x == 0])

        return holes


    def _bumpiness(self, board):
        '''Sum of the differences of heights between pair of columns'''
        total_bumpiness = 0
        max_bumpiness = 0
        min_ys = []

        for col in zip(*board):
            i = 0
            while i < Tetris.HEIGHT and col[i] != 1:
                i += 1
            min_ys.append(i)
        
        for i in range(len(min_ys) - 1):
            bumpiness = abs(min_ys[i] - min_ys[i+1])
            max_bumpiness = max(bumpiness, max_bumpiness)
            total_bumpiness += abs(min_ys[i] - min_ys[i+1])

        return total_bumpiness, max_bumpiness


    def _height(self, board):
        '''Sum and maximum height of the board'''
        sum_height = 0
        max_height = 0
        min_height = Tetris.HEIGHT

        for col in zip(*board):
            i = 0
            while i < Tetris.HEIGHT and col[i] == 0:
                i += 1
            height = Tetris.HEIGHT - i
            sum_height += height
            if height > max_height:
                max_height = height
            elif height < min_height:
                min_height = height

        return sum_height, max_height, min_height


    def get_game_state(self, board):
        lines, board = self._clear_lines(board)
        holes = self._number_of_holes(board)
        total_bumpiness, max_bumpiness = self._bumpiness(board)
        sum_height, max_height, min_height = self._height(board)
        return [lines, holes, total_bumpiness, sum_height]


    def get_action_space(self):
        return 4


    def get_next_states(self):
        '''Get all possible next states'''
        states = {}
        piece_id = self.current_piece.index
        rotations = len(self.current_piece.shape)

        # if piece_id == 3: 
        #     rotations = [0]
        # elif piece_id == 0:
        #     rotations = [0, 90]
        # else:
        #     rotations = [0, 90, 180, 270]

        # For all rotations
        for rotation in range(rotations):
            piece = Piece(Tetris.SHAPES[piece_id], piece_id, rotation=rotation)
            # piece = Tetris.SHAPES[piece_id][rotation]
            min_x = min([p[0] for p in piece.shape[piece.rotation]])
            max_x = max([p[0] for p in piece.shape[piece.rotation]])

            # For all positions
            for x in range(-min_x, Tetris.WIDTH - max_x):
                piece.x = x
                piece.y = 0

                # Drop piece
                while not self._check_collision(piece.shape[piece.rotation], [piece.x, piece.y]):
                    piece.y += 1
                piece.y -= 1

                # Valid move
                if piece.y >= 0:
                    board = self.merge(piece)
                    # Add a way to return reward
                    states[(x, rotation)] = self.get_game_state(board)


        return states


    def render(self):
        # Renders the current board

        img = [Tetris.COLORS[p] for row in self.merge(self.current_piece) for p in row]
        img = np.array(img).reshape(Tetris.HEIGHT, Tetris.WIDTH, 3).astype(np.uint8)
        img = img[..., ::-1] # Convert RRG to BGR (used by cv2)
        img = Image.fromarray(img, 'RGB')
        img = img.resize((Tetris.WIDTH * 25, Tetris.HEIGHT * 25))
        img = np.array(img)
        cv2.putText(img, str(self.score), (22, 22), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        cv2.imshow('image', np.array(img))
        cv2.waitKey(1)