from globals import *
from abc import ABC, abstractmethod
import random
from base_sprites import BaseSprite, BaseCharacter
from text_sprite import TextSprite
from pygame import PixelArray

sprites_to_render_first = pygame.sprite.Group()
sprites_to_render_second = pygame.sprite.Group()
sprites_to_render_third = pygame.sprite.Group()
sprites_to_render_fourth = pygame.sprite.Group()

class Foo(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Harmable(ABC):
    # This is a mixin that handles hit points and damage

    damage_alert_color = WHITE
    stunnable = True

    def get_knockback_vector(self, weapon):
        knockback_vector = vec(self.rect.center) - vec(weapon.rect.center)
        knockback_vector = knockback_vector.normalize()
        return knockback_vector


    def take_damage_from(self, weapon):

        if weapon.is_damage_cooldown_expired(self):
            # randomize damage by 12% in either direction
            real_damage = int(weapon.damage * (1 + random.uniform(-0.12, 0.12)))
            self.hit_points -= real_damage
            weapon.start_cooldown_timer(self)

            # stun the sprite for a bit
            if self.stunnable:
                self.stun(200)

            # make some text appear above the sprite that shows how much damage it took
            damage_alert = TextSprite(
                text=str(real_damage),
                position=(self.rect.midtop[0] + 8, self.rect.midtop[1] - 30),
                font_size=36,
                color=self.damage_alert_color,
                dissolve_timer=500,
            )
            sprites_to_render_fourth.add(damage_alert)

            self.after_damage_taken()

            # if the sprite has no hit points left, kill it
            if self.hit_points <= 0:
                self.die()
        else:
            # print(f"{weapon} cannot hurt {self} because it's on cooldown!")
            return

    def after_damage_taken(self):
        pass

    @abstractmethod
    def die(self):
        pass

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


