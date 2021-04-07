from gym import Env
from gym.spaces import Discrete, Box
from tetris import MyGame
import arcade

class TetrisEnv(Env):

    def __init__(self):
        # Actions we can take: left, right, up, down
        self.action_space = Discrete(4)

        self.game = MyGame()
        self.game.setup()
        arcade.run()

    def step(self, action):
        pass
    
    def render(self):
        pass

    def reset(self):
        pass

env = TetrisEnv()
