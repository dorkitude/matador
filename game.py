import sys
import random
import itertools
from time import sleep
from math import ceil
from globals import *
from sprites import Player, Enemy

# Initialize Pygame
pygame.init()

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title
pygame.display.set_caption("Matador Sandbox")

# initial state
def setup_background():
    tile = pygame.image.load("sprites/desert_tile.png")
    brick_width = tile.get_width()
    brick_height = tile.get_height()
    for x,y in itertools.product(range(0,ceil(800/brick_width)), range(0,ceil(600/brick_height))):
        screen.blit(tile, (x*brick_width, y*brick_height))


# make the player
player = Player()
player.x = 100
player.y = 300

# make the enemies group
enemies = pygame.sprite.Group()

def spawn_enemy():
    print("spawning an enemy")

    spawn_count = random.randint(1,3)

    for i in range(spawn_count):
        enemy = Enemy()
        enemy.x = random.randint(400,700)
        enemy.y = random.randint(300,500)
        enemies.add(enemy)


pygame.time.set_timer(EVENT_SPAWNER_COOLDOWN, 5000)

spawn_enemy()
# Run the game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == EVENT_SPAWNER_COOLDOWN:
            spawn_enemy()

        # For events that occur upon clicking the mouse (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        # Event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
                pass

    # Handle key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        vel_x = -1  # Move left
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        vel_x = 1  # Move right
    else:
        vel_x = 0  # Stop movement
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        vel_y = -1  # Move up
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        vel_y = 1  # Move down
    else:
        vel_y = 0  # Stop movement


    # Update the game state
    # ...

    velocity = vec(vel_x, vel_y)

    if velocity.length() > 0:
        player.move(velocity)

    # Update the display
    setup_background()
    screen.blit(player.image, player.position)

    for enemy in enemies.sprites():
        if enemy.collides_with(player):
            player.take_damage_from(enemy)

        for weapon in player.weapons:
            if enemy.collides_with(weapon):
                enemy.take_damage_from(weapon)

        enemy.pursue(player)
        screen.blit(enemy.image, enemy.position)

    pygame.display.update()

    # Wait for the next frame
    pygame.time.delay(frame_duration)