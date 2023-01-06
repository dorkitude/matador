import sys
import random
import pygame
from math import ceil
import itertools
from sprites import Player, Enemy, Weapon, Halo, sprites_to_render_first, sprites_to_render_second, sprites_to_render_third, sprites_to_render_fourth
from globals import *


class Control(object):
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)
    pygame.init()
    # Create the window
    self.screen = pygame.display.set_mode(window_size)

  # Set the title
    pygame.display.set_caption("Matador Sandbox")

    # make the player
    player = Player(x=100, y=250)
    sprites_to_render_second.add(player)
    self.player = player

  def update(self):
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == EVENT_SPAWNER_COOLDOWN:
            self.spawn_enemies()

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
    player = self.player

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
        enemy.update(player)
        Enemy.resolved_enemies.add(enemy)


  def setup_background(self):
    tile = pygame.image.load("sprites/desert_tile.png")
    brick_width = tile.get_width()
    brick_height = tile.get_height()
    for x,y in itertools.product(range(0,ceil(window_size[0]/brick_width)), range(0,ceil(window_size[1]/brick_height))):
        self.screen.blit(tile, (x*brick_width, y*brick_height))

  def spawn_enemies(self):
    Enemy.spawn_enemies()