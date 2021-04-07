"""
Tetris

Tetris clone, with some ideas from silvasur's code:
https://gist.github.com/silvasur/565419/d9de6a84e7da000797ac681976442073045c74a4

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.tetris
"""
import arcade
import random
import PIL

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, render=True):
        """ Set up the application. """

        self.render = render

        self.row_count = 22
        self.column_count = 10
        self.block_width = 25
        self.block_height = 25
        self.margin = 2
        screen_width = (self.block_width + self.margin) * self.column_count + self.margin
        self.screen_height = (self.block_height + self.margin) * self.row_count
        title = "Tetris"

        self.colors = [
          (0,   0,   0),
          (255, 0,   0),
          (0,   150, 0),
          (0,   0,   255),
          (255, 120, 0),
          (255, 255, 0),
          (180, 0,   255),
          (0,   220, 220)
          ]

        self.tetris_shapes = [
            [[1, 1, 1],
            [0, 1, 0]],

            [[0, 2, 2],
            [2, 2, 0]],

            [[3, 3, 0],
            [0, 3, 3]],

            [[4, 0, 0],
            [4, 4, 4]],

            [[0, 0, 5],
            [5, 5, 5]],

            [[6, 6, 6, 6]],

            [[7, 7],
            [7, 7]]
        ]

        self.texture_list = self.create_textures()

        if self.render:
            super().__init__(screen_width, self.screen_height, title)
            arcade.Window.center_window(self)
            arcade.set_background_color(arcade.color.WHITE)

        self.board = None
        self.frame_count = 0
        self.game_over = False
        self.paused = False
        self.board_sprite_list = None

        self.stone = None
        self.stone_x = 0
        self.stone_y = 0

    def create_textures(self):
        """ Create a list of images for sprites based on the global colors. """
        new_textures = []
        for color in self.colors:
            # noinspection PyUnresolvedReferences
            image = PIL.Image.new('RGB', (self.block_width, self.block_height), color)
            new_textures.append(arcade.Texture(str(color), image=image))
        return new_textures

    def rotate_counterclockwise(self, shape):
        """ Rotates a matrix clockwise """
        return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]


    def check_collision(self, shape, offset):
        """
        See if the matrix stored in the shape will intersect anything
        on the board based on the offset. Offset is an (x, y) coordinate.
        """
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                if cell and self.board[cy + off_y][cx + off_x]:
                    return True
        return False


    def remove_row(self, row):
        """ Remove a row from the board, add a blank row on top. """
        del self.board[row]
        return [[0 for _ in range(self.column_count)]] + self.board


    def join_matrixes(self, matrix_1, matrix_2, matrix_2_offset):
        """ Copy matrix 2 onto matrix 1 based on the passed in x, y offset coordinate """
        offset_x, offset_y = matrix_2_offset
        for cy, row in enumerate(matrix_2):
            for cx, val in enumerate(row):
                matrix_1[cy + offset_y - 1][cx + offset_x] += val
        return matrix_1


    def new_board(self):
        """ Create a grid of 0's. Add 1's to the bottom for easier collision detection. """
        # Create the main board of 0's
        self.board = [[0 for _x in range(self.column_count)] for _y in range(self.row_count)]
        # Add a bottom border of 1's
        self.board += [[1 for _x in range(self.column_count)]]

    def new_stone(self):
        """
        Randomly grab a new stone and set the stone location to the top.
        If we immediately collide, then game-over.
        """
        self.stone = random.choice(self.tetris_shapes)
        self.stone_x = int(self.column_count / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        if self.check_collision(self.stone, (self.stone_x, self.stone_y)):
            self.game_over = True
            print("Game Over")

    def setup(self):
        self.new_board()
        self.board_sprite_list = arcade.SpriteList()
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                sprite = arcade.Sprite()
                for texture in self.texture_list:
                    sprite.append_texture(texture)
                sprite.set_texture(0)
                sprite.center_x = (self.margin + self.block_width) * column + self.margin + self.block_width // 2
                sprite.center_y = self.screen_height - (self.margin + self.block_height) * row + self.margin + self.block_height // 2

                self.board_sprite_list.append(sprite)

        self.new_stone()
        self.update_board()

    def drop(self):
        """
        Drop the stone down one place.
        Check for collision.
        If collided, then
          join matrixes
          Check for rows we can remove
          Update sprite list with stones
          Create a new stone
        """
        if not self.game_over and not self.paused:
            self.stone_y += 1
            if self.check_collision(self.stone, (self.stone_x, self.stone_y)):
                self.board = self.join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = self.remove_row(i)
                            break
                    else:
                        break
                self.update_board()
                self.new_stone()

    def rotate_stone(self):
        """ Rotate the stone, check collision. """
        if not self.game_over and not self.paused:
            new_stone = self.rotate_counterclockwise(self.stone)
            if self.stone_x + len(new_stone[0]) >= self.column_count:
                self.stone_x = self.column_count - len(new_stone[0])
            if not self.check_collision(new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def on_update(self, dt):
        """ Update, drop stone if warrented """
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.drop()
        
        for i in range(0,len(self.board)):
            print(self.board[i])
        print("\n")

        for i in range(0,len(self.stone)):
            print(self.stone[i])

        print("\n\n\n\n")

    def move(self, delta_x):
        """ Move the stone back and forth based on delta x. """
        if not self.game_over and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > self.column_count - len(self.stone[0]):
                new_x = self.column_count - len(self.stone[0])
            if not self.check_collision(self.stone, (new_x, self.stone_y)):
                self.stone_x = new_x

    def on_key_press(self, key, modifiers):
        """
        Handle user key presses
        User goes left, move -1
        User goes right, move 1
        Rotate stone,
        or drop down
        """
        if key == arcade.key.LEFT:
            self.move(-1)
        elif key == arcade.key.RIGHT:
            self.move(1)
        elif key == arcade.key.UP:
            self.rotate_stone()
        elif key == arcade.key.DOWN:
            self.drop()

    # noinspection PyMethodMayBeStatic
    def draw_grid(self, grid, offset_x, offset_y):
        """
        Draw the grid. Used to draw the falling stones. The board is drawn
        by the sprite list.
        """
        # Draw the grid
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                # Figure out what color to draw the box
                if grid[row][column]:
                    color = self.colors[grid[row][column]]
                    # Do the math to figure out where the box is
                    x = (self.margin + self.block_width) * (column + offset_x) + self.margin + self.block_width // 2
                    y = self.screen_height - (self.margin + self.block_height) * (row + offset_y) + self.margin + self.block_height // 2

                    # Draw the box
                    arcade.draw_rectangle_filled(x, y, self.block_width, self.block_height, color)

    def update_board(self):
        """
        Update the sprite list to reflect the contents of the 2d grid
        """
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                v = self.board[row][column]
                i = row * self.column_count + column
                self.board_sprite_list[i].set_texture(v)

    def on_draw(self):
        """ Render the screen. """
        if self.render:
            # This command has to happen before we start drawing
            arcade.start_render()
            self.board_sprite_list.draw()
            self.draw_grid(self.stone, self.stone_x, self.stone_y)

