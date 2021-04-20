from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
from tetris import MyGame
import arcade

class TetrisEnv(Env):

    """
    Observation:
        None

    Actions:
        Type: Discrete(5)
        Num   Action
        0     Push shape left
        1     Push shape right
        2     Push shape down
        3     Rotate shape

    Reward:
        Reward is 1 for every row is completed

    Starting State:
        Empty board

    Episode Termination:
        A shape fills the top square in the play area.
    """

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
