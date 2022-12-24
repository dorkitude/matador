import sys
import code
import itertools
from globals import *
from models import Foo, Player
from time import sleep
from math import ceil

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


# Make the ball
ball = Foo()
ball.radius = 20
ball.x = 300
ball.y = 200
ball.vel_x = 5  # Initial velocity (move right)
ball.vel_y = 5  # Initial velocity (move down)

# make the player
player = Player()
player.width = 64
player.height = 64
player.x = 100
player.y = 300
player.vel_x = 0  # Initial velocity (no movement)
player.vel_y = 0  # Initial velocity (no movement)

# colors
ball.color = (200, 200, 200)

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
        player.vel_x = -5  # Move left
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.vel_x = 5  # Move right
    else:
        player.vel_x = 0  # Stop movement
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.vel_y = -5  # Move up
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.vel_y = 5  # Move down
    else:
        player.vel_y = 0  # Stop movement

    # Update the playet position
    player.x += player.vel_x
    player.y += player.vel_y

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

    # Update the ball position
    ball.x += ball.vel_x
    ball.y += ball.vel_y

    # Check for ball collision with the walls
    if ball.x - ball.radius < 0 or ball.x + ball.radius > window_size[0]:
        ball.vel_x *= -1  # Reverse the horizontal velocity
    if ball.y - ball.radius < 0 or ball.y + ball.radius > window_size[1]:
        ball.vel_y *= -1  # Reverse the vertical velocity

    # Draw the player
    # Calculate the points of the U-shaped player
    # code.interact(local=dict(globals(), **locals()))
    screen.blit(player.image, player.position)

    # Draw the playet
    # pygame.draw.polygon(screen, player.color, player.points)


    # Draw the ball
    pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.radius)


    pygame.display.update()


    # Wait for the next frame
    pygame.time.delay(frame_duration)
