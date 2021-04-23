class Piece(object):
    def __init__(self, x, y, shape, rotation=0):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = rotation

    def rotate_clockwise(self):
        max_rotations = len(self.shape)-1
        self.rotation += 1
        if self.rotation > max_rotations:
            self.rotation = 0
    
    def get_offsets(self):
        x_offset = len(self.shape[self.rotation][0])
        y_offset = len(self.shape[self.rotation])
        return x_offset, y_offset