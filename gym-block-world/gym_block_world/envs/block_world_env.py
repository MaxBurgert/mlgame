import gym
import random
from gym import error, spaces, distutils
from gym.utils import seeding


# Example state
############
# -x-------#
# ---------#
# -----o---#
# ---------#
# ---------#
############

class StateSpace:

    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.pos_agent = self.calc_pos_agent()
        self.pos_goal = self.calc_pos_goal()
        self.pos_obstacle = self.calc_pos_obstacle()

    def calc_pos_agent(self):
        return self._calc_pos()

    def calc_pos_goal(self):
        pos_x, pos_y = self._calc_pos()
        while (pos_x, pos_y) == self.pos_agent:
            pos_x, pos_y = self._calc_pos()
        return pos_x, pos_y

    def calc_pos_obstacle(self):
        pos_x, pos_y = self._calc_pos()
        while (pos_x, pos_y) == self.pos_agent or (pos_x, pos_y) == self.pos_goal:
            pos_x, pos_y = self._calc_pos()
        return pos_x, pos_y

    def _calc_pos(self):
        pos_x = random.randint(0, self.width)
        pos_y = random.randint(0, self.length)
        return pos_x, pos_y


class BlockWorldEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.done = 0
        self.counter = 0
        self.state = StateSpace(8,8)
        self.reward = 0

    def step(self, action):
        if self.done == 1:
            print("Game Over")

        win = 0
        if win:
            self.done = 1
            print("Win")

    def reset(self):
        self.done = 0
        self.counter = 0

    def render(self, mode='human', close=False):
        for i in range(8+1):
            for j in range(8+1):
                if (self.state.pos_agent) == (i,j):
                    print('x', end=' ')
                elif (self.state.pos_goal) == (i,j):
                    print('o', end=' ')
                elif (self.state.pos_obstacle) == (i, j):
                    print('#', end=' ')
                else:
                    print('-', end=' ')
            print(" ")
