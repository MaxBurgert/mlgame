import pygame

pygame.init()
screen = pygame.display.set_mode((500,500))
done = False

x = 30
y = 30
rect_size = 30
move_distance = 2
position_goal_x = 400
position_goal_y = 400

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

    #
    if 400 <= (x + rect_size) <= (400 + rect_size):
        if 400 <= (y + rect_size) <= (400 + rect_size):
            done = True

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (200, 28, 0), pygame.Rect(position_goal_x, position_goal_y, rect_size, rect_size))
    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x, y, rect_size, rect_size))

    pygame.display.flip()
    clock.tick(60)
