import sys
import random
import itertools
from math import ceil
from globals import *
from sprites import Player, Enemy, Weapon, Halo, sprites_to_render_first, sprites_to_render_second, sprites_to_render_third
import ui

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
    for x,y in itertools.product(range(0,ceil(window_size[0]/brick_width)), range(0,ceil(window_size[1]/brick_height))):
        screen.blit(tile, (x*brick_width, y*brick_height))


# make the player
player = Player()
player.x = 100
player.y = 250
sprites_to_render_second.add(player)

# make the starting weapon
halo = Halo(player, STARTING_HALO_RADIUS)
sprites_to_render_first.add(halo)

def spawn_enemy():
    # Ramp:  every 5 seconds since launch, increase the spawn rate
    spawn_count = random.randint(1,3)
    seconds_since_launch = now() - start_time
    spawn_count += 2*int(seconds_since_launch / 5000)

    # print(f"spawning {spawn_count} enemies")
    zone_topleft = (750, 50)
    zone_bottomright = (950, 700)

    for i in range(spawn_count):
        enemy = Enemy()
        enemy.x = random.randint(zone_topleft[0], zone_bottomright[0])
        enemy.y = random.randint(zone_topleft[1], zone_bottomright[1])

        # try not to let this enemy overlap with any others
        placement_tries = 10
        tries_attempted = 0
        skip_this_enemy = False
        while tries_attempted < placement_tries and enemy.collides_with_any(Enemy.all_enemies):
            tries_attempted += 1
            print(f"attempt {tries_attempted} collided: {enemy.collides_with_any(Enemy.all_enemies).rect}")
            enemy.x = random.randint(zone_topleft[0], zone_bottomright[0])
            enemy.y = random.randint(zone_topleft[1], zone_bottomright[1])
            if tries_attempted == placement_tries:
                skip_this_enemy = True

        if skip_this_enemy:
            enemy.kill()
            continue
        else:
            sprites_to_render_third.add(enemy)
            Enemy.all_enemies.add(enemy)
            Enemy.pursuing_enemies.add(enemy)

# this schedules a reccurring event to spawn enemies
pygame.time.set_timer(EVENT_SPAWNER_COOLDOWN, ceil(1000*GLOBAL_SPAWN_RATE))

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

    # Handle WASD and Arrow-key input
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

    player_velocity = vec(vel_x, vel_y)

    # Update the game state

    # check for damage
    for enemy in Enemy.all_enemies.sprites():
        if enemy.collides_with(player):
            player.take_damage_from(enemy)

        for weapon in Weapon.all_weapons.sprites():
            if weapon.collides_with(enemy):
                enemy.take_damage_from(weapon)

    # Move the player
    if player_velocity.length() > 0:
        player.move(player_velocity)

    all_enemies = Enemy.all_enemies.sprites()

    # sort the enemies by distance to the player
    all_enemies = sorted(all_enemies, key=lambda enemy: enemy.distance_to(player))

    # make a group of enemies whose movement is resolved
    Enemy.resolved_enemies = pygame.sprite.Group()

    # move the enemies
    for enemy in all_enemies:
        enemy.pursue(player)
        Enemy.resolved_enemies.add(enemy)

    # -------------------
    # Update the display
    # -------------------

    # show/update player HP bar in top-peft
    ui.render_player_stats(player)

    # first, handle map and background stuff
    setup_background()

    # next, render floor-level stuff
    for sprite in sprites_to_render_first:
        sprite.render(screen)

    for sprite in sprites_to_render_second:
        sprite.render(screen)

    for sprite in sprites_to_render_third:
        sprite.render(screen)

    # for weapon in Weapon.all_weapons.sprites():
    #     weapon.render(screen)

    # player.render(screen)

    # for enemy in Enemy.all_enemies.sprites():
    #     enemy.render(screen)

    pygame.display.update()

    Enemy.resolved_enemies.empty()

    # Wait for the next frame
    pygame.time.delay(frame_duration)