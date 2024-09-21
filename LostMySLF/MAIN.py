import pygame
import math

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LostMySLFL")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

world_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

TILE_SIZE = 64
MAP_WIDTH = len(world_map[0])
MAP_HEIGHT = len(world_map)

player_x = TILE_SIZE * 1.5
player_y = TILE_SIZE * 1.5
player_angle = 0
player_fov = math.pi / 3

player_speed = 2

texture_front_back = pygame.image.load('IMG/wall_texture.png')
texture_left_right = pygame.image.load('IMG/wall_texture2.png')

def cast_ray(x, y, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    for depth in range(0, 300):
        target_x = x + cos_a * depth
        target_y = y + sin_a * depth

        col = int(target_x / TILE_SIZE)
        row = int(target_y / TILE_SIZE)

        if col >= 0 and col < MAP_WIDTH and row >= 0 and row < MAP_HEIGHT:
            if world_map[row][col] == 1:
                return depth, target_x % TILE_SIZE, target_y % TILE_SIZE, col, row
    return None, None, None, None, None

def draw_3d():
    for ray in range(WIDTH):
        ray_angle = player_angle - player_fov / 2 + ray * player_fov / WIDTH
        depth, hit_x, hit_y, col, row = cast_ray(player_x, player_y, ray_angle)

        if depth:
            wall_height = HEIGHT / (depth * math.cos(ray_angle - player_angle)) * 70

            # Визначення сторони стіни
            if abs(hit_x) > abs(hit_y):
                texture_x = int(hit_x * (texture_left_right.get_width() / TILE_SIZE))
                texture_column = texture_left_right.subsurface(texture_x, 0, 1, texture_left_right.get_height())
            else:
                texture_x = int(hit_y * (texture_front_back.get_width() / TILE_SIZE))
                texture_column = texture_front_back.subsurface(texture_x, 0, 1, texture_front_back.get_height())

            texture_column = pygame.transform.scale(texture_column, (1, int(wall_height)))
            screen.blit(texture_column, (ray, HEIGHT // 2 - wall_height // 2))

def move_player():
    global player_x, player_y, player_angle

    keys = pygame.key.get_pressed()

    new_x = player_x
    new_y = player_y

    if keys[pygame.K_w]:
        new_x += math.cos(player_angle) * player_speed
        new_y += math.sin(player_angle) * player_speed
    if keys[pygame.K_s]:
        new_x -= math.cos(player_angle) * player_speed
        new_y -= math.sin(player_angle) * player_speed

    if world_map[int(new_y // TILE_SIZE)][int(new_x // TILE_SIZE)] == 0:
        player_x = new_x
        player_y = new_y

    if keys[pygame.K_a]:
        player_angle -= 0.03
    if keys[pygame.K_d]:
        player_angle += 0.03

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    move_player()

    draw_3d()

    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
