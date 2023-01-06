from globals import *
from sprites import BaseSprite, Harmable, sprites_to_render_first, sprites_to_render_fourth
import pygame
from abc import ABC, abstractmethod

class Weapon(ABC):

    all_weapons = pygame.sprite.Group()

    # This is a mixin that handles anything that can deal damage


    # this is the amount of damage to deal
    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

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

    # this is reported by the Harmable after it takes damage from me
    def report_damage_taken(self, harmable):
        pass

    def start_damage_cooldown_timer(self, target):
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

class MagicWand(BaseSprite, Weapon):
    _damage = 8
    speed = 8
    duration = 2500

    # we'll use this as a firing cooldown for now
    damage_cooldown = 1200
    delay_between_missiles = 150
    missiles_per_volley = 3

    def __init__(self, player, control):
        super().__init__()
        Weapon.all_weapons.add(self)

        self.status = "idle"
        self.player = player
        self.control = control
        self.missiles = pygame.sprite.Group()

        self.fired_this_volley = 0
        self.last_missile_fired = -100000


    def collides_with(self, enemy):
        return False

    def update(self):

        self.rect = self.player.rect
        self.x = self.player.x
        self.y = self.player.y


        # if i'm idle, check to see if the damage cooldown has expired
        # if it has expired, i should resume firing
            # when firing, check if missile cooldown has expired
        # if it hasn't expired, i should stay idle

        if self.status == "idle":
            if self.is_damage_cooldown_expired(self.player):
                print("wand is firing a new volley")
                self.fired_this_volley = 0
                self.start_damage_cooldown_timer(self.player)
                self.status = "firing"

        if self.status == "firing":
            if self.fired_this_volley >= self.missiles_per_volley:
                # i've fired as many as i can this volley
                self.status = "idle"
            else:
                if self.is_delay_between_missiles_expired():
                    self.fire()

    def is_delay_between_missiles_expired(self):
        elapsed = now() - self.last_missile_fired
        if elapsed > self.delay_between_missiles:
            return True
        else:
            return False

    def fire(self):
        # fire a missile
        target = self.control.get_closest_living_enemy(self.player)

        if target is None:
            return False

        missile = Missile(
            shooter=self,
            target=target,
            speed=self.speed,
            damage=self.damage
        )
        self.missiles.add(missile)

        self.last_missile_fired = now()
        self.fired_this_volley += 1

        print(f"missile fired, {self.fired_this_volley} missiles fired this volley")


class Missile(BaseSprite, Weapon):

    image = None

    def __init__(self, shooter, target, speed, damage):
        super().__init__()
        Weapon.all_weapons.add(self)

        self.born = now()
        self.shooter = shooter
        self.duration = self.shooter.duration
        self.target = target
        self.speed = speed
        self.damage = damage

        # save the image to a class variable so we don't have to load it every time
        if Missile.image is None:
            Missile.image = pygame.image.load("sprites/redbubble.png").convert_alpha()
        self.image = Missile.image

        self.rect = self.image.get_rect()
        self.x = shooter.x
        self.y = shooter.y

        self.vector = vec(target.rect.center) - vec(shooter.rect.center)
        self.vector = self.vector.normalize()

        self.after_move()

    def pursue(self, sprite):
        destination_x = sprite.rect.center[0]
        destination_y = sprite.rect.center[1]
        self.direction = vec((destination_x-self.x, destination_y-self.y))
        self.move(self.direction)

    def inertial_move(self):
        # check to see if i have a direction attribute
        if hasattr(self, "direction"):
            self.move(self.direction)
        else:
            self.kill()

    def update(self):

        if now() - self.born > self.duration:
            self.kill()
            return

        sprites_to_render_fourth.add(self)

        if self.target is None:
            print(f"{self} target is gone, finding a new one")
            self.target = self.shooter.control.get_closest_living_enemy(self)
            if self.target is None:
                self.inertial_move()
                return
        if self.target.status == "dying":
            self.inertial_move()
            return

        self.pursue(self.target)
        # print(f"{self} is pursuing target {self.target}")

    # only does damage to one thing, then fizzles
    def report_damage_taken(self, harmable):
        self.kill()

    def __str__(self):
        return f"Missile {self.id}"

class Halo(BaseSprite, Weapon):

    _damage = 10

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