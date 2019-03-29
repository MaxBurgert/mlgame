import random

import gym
from gym import spaces


# Example state
# (0,0) is top left corner
# - - - - - - - - -
# - o - - - - - - -
# - - - - - - - - -
# - - - - - - - - -
# - - - - - - # - -
# - - x - - - - - -
# - - - - - - - - -
# - - - - - - - - -
# - - - - - - - - -


class BlockWorldEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.done = 0
        self.counter = 0
        self.width = 9
        self.height = 9
        self.pos_agent = self.calc_pos_agent()
        self.pos_goal = self.calc_pos_goal()
        self.pos_obstacle = self.calc_pos_obstacle()
        # [shape,agent_pos,obstacle_pos,goal_pos]
        self.state = [self.pos_agent[0], self.pos_agent[1], self.pos_goal[0], self.pos_goal[1],
                      self.pos_obstacle[0], self.pos_obstacle[1], self.pos_obstacle[2], self.pos_obstacle[3],
                      self.pos_obstacle[4], self.pos_obstacle[5]]
        self.reward = 0
        self.add = [0, 0]
        self.action_space = spaces.Discrete(4)

    def calc_pos_agent(self):
        return self._calc_pos()

    def calc_pos_goal(self):
        pos_x, pos_y = self._calc_pos()
        while abs(pos_x - self.pos_agent[0]) <= 1 and abs(pos_y - self.pos_agent[1]) <= 1:
            pos_x, pos_y = self._calc_pos()
        return pos_x, pos_y

    def calc_pos_obstacle(self):
        """
             #       #
            #x#     #x
                     #
            open_pos -> only feasible action for agent
        :return:
        """
        open_pos = random.randint(0, 3)
        if open_pos == 0:
            pos_x_1, pos_y_1 = self.pos_agent[0] + 1, self.pos_agent[1]
            pos_x_2, pos_y_2 = self.pos_agent[0], self.pos_agent[1] + 1
            pos_x_3, pos_y_3 = self.pos_agent[0] - 1, self.pos_agent[1]
        elif open_pos == 1:
            pos_x_1, pos_y_1 = self.pos_agent[0], self.pos_agent[1] + 1
            pos_x_2, pos_y_2 = self.pos_agent[0] - 1, self.pos_agent[1]
            pos_x_3, pos_y_3 = self.pos_agent[0], self.pos_agent[1] - 1
        elif open_pos == 2:
            pos_x_1, pos_y_1 = self.pos_agent[0] - 1, self.pos_agent[1]
            pos_x_2, pos_y_2 = self.pos_agent[0], self.pos_agent[1] - 1
            pos_x_3, pos_y_3 = self.pos_agent[0] + 1, self.pos_agent[1]
        elif open_pos == 3:
            pos_x_1, pos_y_1 = self.pos_agent[0], self.pos_agent[1] - 1
            pos_x_2, pos_y_2 = self.pos_agent[0] + 1, self.pos_agent[1]
            pos_x_3, pos_y_3 = self.pos_agent[0], self.pos_agent[1] + 1
        return pos_x_1, pos_y_1, pos_x_2, pos_y_2, pos_x_3, pos_y_3

    def _calc_pos(self):
        pos_x = random.randint(1, (self.width - 2))  # agent should not spawn on edges
        pos_y = random.randint(1, (self.height - 2))
        return pos_x, pos_y

    def _apply_action(self, action):
        """
        :param action: possible actions: 0 -> up
                                         1 -> right
                                         2 -> down
                                         3 -> left
        :return:
        """
        state_copy = self.state.copy()
        if action == 0:
            state_copy[1] = state_copy[1] - 1
        elif action == 1:
            state_copy[0] = state_copy[0] + 1
        elif action == 2:
            state_copy[1] = state_copy[1] + 1
        elif action == 3:
            state_copy[0] = state_copy[0] - 1
        return state_copy

    def step(self, action):
        if self.done == 1:
            print("Game Over")
            return [self.state, self.reward, self.done, self.add]
        else:
            new_state = self._apply_action(action)
            if new_state[0] < 0 or new_state[0] >= self.width or new_state[1] < 0 or new_state[1] >= self.height:
                self.reward = -10
                self.counter += 1
                return [self.state, self.reward, self.done, self.add]
            else:
                self.state = new_state
                self.counter += 1
                self.reward = -1

            if self.counter == 40:
                self.done = 1

            # self.render()

        win = None
        if self.state[0] == self.state[2] and self.state[1] == self.state[3]:
            win = 1
        if (new_state[0], new_state[1]) == (new_state[4], new_state[5]) or (new_state[0], new_state[1]) == (
                new_state[6], new_state[7]) or (new_state[0], new_state[1]) == (new_state[8], new_state[9]):
            win = -1

        if win:
            self.done = 1
            self.add[win - 1] = 1
            if win == 1:
                self.reward = 200
            else:
                self.reward = -100

        return [self.state, self.reward, self.done, self.add]

    def reset(self):
        self.done = 0
        self.counter = 0
        self.pos_agent = self.calc_pos_agent()
        self.pos_goal = self.calc_pos_goal()
        self.pos_obstacle = self.calc_pos_obstacle()
        # [shape,agent_pos,goal_pos,obstacle_pos]
        self.state = [self.pos_agent[0], self.pos_agent[1], self.pos_goal[0], self.pos_goal[1],
                      self.pos_obstacle[0], self.pos_obstacle[1], self.pos_obstacle[2], self.pos_obstacle[3],
                      self.pos_obstacle[4], self.pos_obstacle[5]]
        self.reward = 0
        self.add = [0, 0]
        return self.state

    def render(self, mode='human', close=False):
        for i in range(self.height):
            for j in range(self.width):
                if self.state[0] == j and self.state[1] == i:
                    print('x', end=' ')
                elif self.state[2] == j and self.state[3] == i:
                    print('o', end=' ')
                elif self.state[4] == j and self.state[5] == i:
                    print('#', end=' ')
                elif self.state[6] == j and self.state[7] == i:
                    print('#', end=' ')
                elif self.state[8] == j and self.state[9] == i:
                    print('#', end=' ')
                else:
                    print('-', end=' ')
            print("")
        print("")
