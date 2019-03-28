import gym
import random
from gym import spaces

# Example state
# - - - - - - - - -
# - o - - - - - - -
# - - - - - - - - -
# - - - - - - - - -
# - - - - - - # - -
# - - x - - - - - -
# - - - - - - - - -
# - - - - - - - - -
# - - - - - - - - -

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

    def apply_action(self, action):
        """
        :param action: possible actions: 0 -> up
                                         1 -> right
                                         2 -> down
                                         3 -> left
        :return:
        """
        if action == 0:
            return self.pos_agent[0] - 1, self.pos_agent[1]
        elif action == 1:
            return self.pos_agent[0], self.pos_agent[1] + 1
        elif action == 2:
            return self.pos_agent[0] + 1, self.pos_agent[1]
        elif action == 3:
            return self.pos_agent[0] - 1, self.pos_agent[1] - 1


class BlockWorldEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.done = 0
        self.counter = 0
        self.state = StateSpace(8, 8)
        self.reward = 0
        self.add = [0, 0]
        self.action_space = spaces.Discrete(4)

    def step(self, action):
        if self.done == 1:
            print("Game Over")
            return [self.state, self.reward, self.done, self.add]
        else:
            new_state = self.state.apply_action(action)
            if new_state[0] < 0 or new_state[0] > 8 or new_state[1] < 0 or new_state[1] > 8:
                print("Invalid Step")
                return [self.state, self.reward, self.done, self.add]
            else:
                self.state.pos_agent = new_state
                self.counter += 1
                if self.counter > 16:
                    self.done = 1
                self.render()

        win = 0
        if self.state.pos_agent == self.state.pos_goal:
            win = 1
        elif self.state.pos_agent == self.state.pos_obstacle:
            win = -1

        if win:
            self.done = 1
            self.add[win - 1] = 1
            if win == 1:
                print("Win")
                self.reward = 100
            else:
                self.reward = -100

        return [self.state, self.reward, self.done, self.add]

    def reset(self):
        self.done = 0
        self.counter = 0
        self.state = StateSpace(8, 8)
        self.reward = 0
        self.add = [0, 0]
        return self.state

    def render(self, mode='human', close=False):
        for i in range(8 + 1):
            for j in range(8 + 1):
                if self.state.pos_agent == (i, j):
                    print('x', end=' ')
                elif self.state.pos_goal == (i, j):
                    print('o', end=' ')
                elif self.state.pos_obstacle == (i, j):
                    print('#', end=' ')
                else:
                    print('-', end=' ')
            print("")
        print("")
