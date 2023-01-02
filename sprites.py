from globals import *
from abc import ABC, abstractmethod
import random
from base_sprites import BaseSprite, BaseCharacter


sprites_to_render_first = pygame.sprite.Group()
sprites_to_render_second = pygame.sprite.Group()
sprites_to_render_third = pygame.sprite.Group()

class Foo(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Harmable(ABC):
    # This is a mixin that handles hit points and damage

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

            # stun the sprite for a bit (player is immune to stun)
            if not isinstance(self, Player):
                self.stun(200)

            # make some text appear above the sprite that shows how much damage it took


            # if the sprite has no hit points left, kill it
            if self.hit_points <= 0:
                self.die()
        else:
            # print(f"{weapon} cannot hurt {self} because it's on cooldown!")
            return

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

class Player(BaseCharacter, Harmable):

    # default values
    hit_points = 100
    speed = PLAYER_BASE_SPEED
    _weapons = None # this will get set the first time the instance property is accessed
    halo = None
    status = None

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/matador.png").convert()
        self.rect = self.image.get_rect()

    def __str__(self):
        return f"Player {self.id}"

    def die(self):
        # print(f"{self} has died")
        self.kill()

    @property
    def weapons(self):
        if self._weapons is None:
            self._weapons = pygame.sprite.Group()
        return self._weapons

    def after_move(self):
        if self.halo:
            self.halo.x = (self.x + self.width/2) - self.halo.radius
            self.halo.y = (self.y + self.height/2) - self.halo.radius

class Halo(BaseSprite, Weapon):

    damage = 10

    def __init__(self, player, radius):
        super().__init__()
        Weapon.all_weapons.add(self)

        self.image = pygame.Surface((radius*2, radius*2))
        self.rect = self.image.get_rect()
        self.radius = radius
        pygame.draw.circle(self.image, (255, 255, 255, 128), (radius, radius), radius)
        player.halo = self
        player.after_move()

    def __str__(self):
        return f"Halo {self.id}"



class Enemy(BaseCharacter, Harmable, Weapon):

    default_status = "pursuing"
    all_enemies = pygame.sprite.Group()
    resolved_enemies = pygame.sprite.Group()
    pursuing_enemies = pygame.sprite.Group()

    speed = 2
    hit_points = 10
    _damage = 1

    def __init__(self):
        super().__init__()

        self.status = self.default_status

        if random.randint(1,10) > 9:
            self.hit_points = 5
            self.image = pygame.image.load("sprites/lizard_f_idle_anim_f3.png").convert_alpha()
        else:
            self.hit_points = 15
            self._damage = 3
            self.image = pygame.image.load("sprites/skull_v1_4.png").convert()
        self.rect = self.image.get_rect()

    @property
    def damage(self):
        return self._damage

    def __str__(self):
        return f"An Enemy {self.id}"

    def pursue(self, sprite):
        if self.is_stunned():
            knockback_vector = self.get_knockback_vector(sprite)
            self.move(knockback_vector, speed_scalar=3)
        else:
            destination_x = sprite.position[0] + random.randint(1,sprite.width)
            destination_y = sprite.position[1] + random.randint(1,sprite.height)
            direction = vec((destination_x-self.x, destination_y-self.y))
            self.move(direction, Enemy.resolved_enemies)

    def die(self):
        print(f"{self} has died")
        self.kill()