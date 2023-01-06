from globals import *
from sprites import BaseSprite, Harmable, sprites_to_render_first
import pygame
from abc import ABC, abstractmethod

class Weapon(ABC):

    all_weapons = pygame.sprite.Group()

    # This is a mixin that handles anything that can deal damage

    # this is the amount of damage to take
    @property
    def damage(self):
        pass

    # Cooldown logic.
    # ----------------------------------------------------
    # A weapon should only be able to hurt a given Harmable once every X milliseconds.
    # That 'X' is called a cooldown.
    damage_cooldown = 1200  # milliseconds
    last_recorded_damage = None

    def is_damage_cooldown_expired(self, target):
        # make sure target is a Harmable
        if not isinstance(target, Harmable):
            raise TypeError(f"target must be a Harmable, not a {type(target)}")

        # Check to see if enough time has ellapsed since we last hit this target.
        elapsed = now() - self.get_last_damage_time(target)

        # print(f"elapsed = {elapsed}, cooldown = {self.damage_cooldown}")

        if elapsed > self.damage_cooldown:
            return True
        else:
            return False

    def start_cooldown_timer(self, target):
        if self.last_recorded_damage is None:
            self.last_recorded_damage = {}
        self.last_recorded_damage[target.id] = now()

    def get_last_damage_time(self, target):
        if self.last_recorded_damage is None:
            self.last_recorded_damage = {}

        if target.id in self.last_recorded_damage:
            return self.last_recorded_damage[target.id]
        else:
            return -10000000 # give a time in the past


class Halo(BaseSprite, Weapon):

    damage = 10

    def __init__(self, player, radius):
        super().__init__()
        Weapon.all_weapons.add(self)

        self.image = pygame.Surface((radius*2, radius*2))
        self.rect = self.image.get_rect()
        self.radius = radius
        pygame.draw.circle(self.image, SOFT_YELLOW, (radius, radius), radius)
        player.halo = self
        player.after_move()

    def collides_with(self, sprite):
        super_collider = super().collides_with(sprite)

        # check if my circle collides with the sprite's rect
        if super_collider:

            # check if the sprite's rect is inside the circle
            circle_x = self.rect.center[0]
            circle_y = self.rect.center[1]
            radius = self.radius

            # find which corner of the rect is closest to the center of the circle
            dx = abs(circle_x - sprite.x - sprite.rect.width / 2)
            dy = abs(circle_y - sprite.y - sprite.rect.height / 2)
            if dx > sprite.rect.width / 2 + self.radius:
                return False
            elif dy > sprite.height / 2 + self.radius:
                return False
            else:
                if dx <= sprite.rect.width / 2:
                    return True
                elif dy <= sprite.rect.height / 2:
                    return True
                else:
                    corner_distance_sq = (dx - sprite.rect.width / 2) ** 2 + (dy - sprite.rect.height / 2) ** 2
                    if corner_distance_sq <= self.radius ** 2:
                        return True
                    else:
                        return False

        return False

    def __str__(self):
        return f"Halo {self.id}"