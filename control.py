import sys
import random
import pygame
from math import ceil
import itertools
from sprites import sprites_to_render_first, sprites_to_render_second, sprites_to_render_third, sprites_to_render_fourth
from weapons import Weapon, Halo, MagicWand
from enemy import Enemy
from player import Player
from globals import *
from hud import Hud


class Control(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        pygame.init()
        # Create the window
        self.screen = pygame.display.set_mode(window_size)

        self.active_sprites = pygame.sprite.Group()

        # Set the title
        pygame.display.set_caption("Matador Sandbox")

        # establish the hud
        self.hud = Hud()

        # make the player
        player = Player(x=100, y=250)
        sprites_to_render_second.add(player)
        self.player = player
        player.control = self

        # make the starting weapons
        player.halo = Halo(player, STARTING_HALO_RADIUS)
        sprites_to_render_first.add(player.halo)

        player.wand = MagicWand(player, self)

        player.hurt_sound = pygame.mixer.Sound("sounds/ouch.wav")

    def update(self):
        player = self.player

        # Handle events
        # -------------
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
        self.player.velocity = self.get_velocity_from_keyboard()

        # Update the game state
        # ---------------------

        # check for damage
        for enemy in Enemy.living_enemies.sprites():
            if enemy.collides_with(player):
                player.take_damage_from(enemy)

            for weapon in Weapon.all_weapons.sprites():
                if weapon.collides_with(enemy):
                    enemy.take_damage_from(weapon)

        # update weapons
        for weapon in Weapon.all_weapons.sprites():
            weapon.update()

        # Move the player
        player.update(self)

        # sort the enemies by distance to the player
        all_enemies = sorted(Enemy.all_enemies.sprites(), key=lambda enemy: enemy.distance_to(player))

        # make a group of enemies whose movement is resolved
        Enemy.resolved_enemies = pygame.sprite.Group()

        # move the enemies
        for enemy in all_enemies:
            enemy.update(self)
            Enemy.resolved_enemies.add(enemy)

    def get_closest_living_enemy(self, thing):
        enemies = sorted(Enemy.living_enemies.sprites(), key=lambda enemy: enemy.distance_to(thing))
        if enemies:
            return enemies[0]
        else:
            return None

    def get_velocity_from_keyboard(self):
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

        return vec(vel_x, vel_y)

    def setup_background(self):
        tile = pygame.image.load("sprites/desert_tile.png")
        brick_width = tile.get_width()
        brick_height = tile.get_height()
        for x,y in itertools.product(range(0,ceil(window_size[0]/brick_width)), range(0,ceil(window_size[1]/brick_height))):
            self.screen.blit(tile, (x*brick_width, y*brick_height))

    def spawn_enemies(self):
        Enemy.spawn_enemies()