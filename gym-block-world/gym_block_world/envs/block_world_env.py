import gym
from gym import error, spaces, distutils
from gym.utils import seeding


class BlockWorldEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.done = 0

    def step(self, action):
        if self.done == 1:
            print("Game Over")

    def reset(self):
        ...

    def render(self, mode='human', close=False):
        ...
