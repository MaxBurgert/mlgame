import gym
from gym import error, spaces, distutils
from gym.utils import seeding
import pygame

pygame.init()
screen = pygame.display.set_mode((88,80))
done = False

x = 2
y = 2
rect_size = 2
move_distance = 1
position_goal_x = 30
position_goal_y = 30
position_obstacle_x = 15
position_obstacle_y = 10

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]: y -= move_distance
    if pressed[pygame.K_s]: y += move_distance
    if pressed[pygame.K_a]: x -= move_distance
    if pressed[pygame.K_d]: x += move_distance

    if position_obstacle_x <= (x + rect_size) <= (position_obstacle_x + rect_size):
        if position_obstacle_y <= (y + rect_size) <= (position_obstacle_y + rect_size):
            done = True

    if position_goal_x <= (x + rect_size) <= (position_goal_x + rect_size):
        if position_goal_y <= (y + rect_size) <= (position_goal_y + rect_size):
            done = True

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (200, 28, 0), pygame.Rect(position_obstacle_x, position_obstacle_y, rect_size, rect_size))
    pygame.draw.rect(screen, (50, 255, 50), pygame.Rect(position_goal_x, position_goal_y, rect_size, rect_size))
    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x, y, rect_size, rect_size))

    pygame.display.flip()
    clock.tick(60)

class BlockWorldEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        ...

    def step(self, action):
        ...

    def reset(self):
        ...

    def render(self, mode='human', close=False):
        ...