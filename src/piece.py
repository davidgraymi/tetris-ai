class Piece(object):
    def __init__(self, x, y, shape):
        # shapes formats

        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = 0

    def rotate(self):
        max_rotations = len(self.shape)-1
        self.rotation += 1
        if self.rotation > max_rotations:
            self.rotation = 0
    
    # def move_left(self, left):
    #     if self.x > left:
    #         self.x -= 1

    def get_offsets(self):
        # print('rotation:{}'.format(self.rotation))
        # print('3dshape:{}'.format(self.shape))
        # print('2dshape:{}'.format(self.shape[self.rotation]))
        x_offset = len(self.shape[self.rotation][0])
        y_offset = len(self.shape[self.rotation])
        # print('x_offset:{} y_offset:{}'.format(x_offset, y_offset))
        return x_offset, y_offset