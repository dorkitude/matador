import sys
import code
import itertools
from time import sleep
from math import ceil
from globals import *
from sprites import Player, Foo

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (800, 600)

pink = (255, 64, 64)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title
pygame.display.set_caption("Matador Sandbox")

# Set the frame rate
frame_rate = 60
frame_duration = int(1000 / frame_rate)

# initial state
def setup_background():
    screen.fill((pink))
    tile = pygame.image.load("sprites/desert_tile.png")
    brick_width = tile.get_width()
    brick_height = tile.get_height()
    for x,y in itertools.product(range(0,ceil(800/brick_width)), range(0,ceil(600/brick_height))):
        # print(f"attempting to draw at {x},{y}")
        # code.interact(local=dict(globals(), **locals()))
        screen.blit(tile, (x*brick_width, y*brick_height))


# make the player
player = Player()
player.x = 100
player.y = 300
player.vel_x = 0  # Initial velocity (no movement)
player.vel_y = 0  # Initial velocity (no movement)

# Run the game loop
running = True
while running:
    setup_background()
  # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()


    # For events that occur upon clicking the mouse (left click)
    if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    # Event handling for a range of different key presses
    if event.type == pygame.KEYDOWN:
            pass

    # Handle key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        vel_x = -player.speed  # Move left
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        vel_x = player.speed  # Move right
    else:
        vel_x = 0  # Stop movement
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        vel_y = -player.speed  # Move up
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        vel_y = player.speed  # Move down
    else:
        vel_y = 0  # Stop movement

    player.velocity = vec(vel_x, vel_y)

    # Update the playet position
    new_position = player.position + player.velocity
    player.x = new_position[0]
    player.y = new_position[1]

    # Keep the player within the window boundaries
    if player.x < 0:
        player.x = 0
    if player.x + player.width > window_size[0]:
        player.x = window_size[0] - player.width
    if player.y < 0:
        player.y = 0
    if player.y + player.height > window_size[1]:
        player.y = window_size[1] - player.height


    # Update the game state
    # ...

    screen.blit(player.image, player.position)

    print(f"player.position = {player.position}")



    pygame.display.update()


    # Wait for the next frame
    pygame.time.delay(frame_duration)
