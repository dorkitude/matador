from globals import *
import random
from abc import ABC, abstractmethod

class Foo(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class BaseSprite(pygame.sprite.Sprite, ABC):
    _width = None
    _height = None

    @property
    def id(self):
        return id(self)

    @property
    def width(self):
        if self._width is None:
            self._width = self.image.get_width()
        return self._width

    @property
    def height(self):
        if self._height is None:
            self._height = self.image.get_height()
        return self._height

    def collides_with(self, sprite): #bool
        return self.rect.colliderect(sprite.rect)

    def move(self, direction):   # void

        if direction.length() == 0:
            return

        # Normalize the direction vector, so we have have a vector of length 1
        direction = direction.normalize()
        magnitude = self.speed * SPEED_MODIFIER * frame_duration

        velocity = vec(direction[0]*magnitude, direction[1]*magnitude)

        new_position = vec(self.x, self.y) + vec(velocity)
        # print(f"velocity:  {velocity}.  position:  {self.position}.  new_position:  {new_position}")
        self.x = new_position[0]
        self.y = new_position[1]
        self.rect.x = self.x
        self.rect.y = self.y

        # Keep the sprite within the window boundaries
        if self.x < 0:
            self.x = 0
        if self.x + self.width > window_size[0]:
            self.x = window_size[0] - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > window_size[1]:
            self.y = window_size[1] - self.height

    def move_toward(self, destination):
        direction = vec((destination[0]-self.x, destination[1]-self.y))
        # print(f"direction = {direction}")
        self.move(direction)

    @property
    def position(self):
        return (self.x, self.y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = value
class Harmable(ABC):
    # This is a mixin that handles hit points and damage

    def take_damage_from(self, weapon):

        if weapon.is_damage_cooldown_expired(self):
            self.hit_points -= weapon.damage
            weapon.start_cooldown_timer(self)
            print(f"{self} is taking {weapon.damage} damage from {weapon} and now has {self.hit_points} hit_points")
            if self.hit_points <= 0:
                self.die()
        else:
            # print(f"{weapon} cannot hurt {self} because it's on cooldown!")
            return


    @abstractmethod
    def die(self):
        pass

class Weapon(ABC):
    # This is a mixin that handles anything that can deal damage



    # this is the amount of damage to take
    @property
    def damage(self):
        pass

    # Cooldown logic.
    # ----------------------------------------------------
    # A weapon should only be able to hurt a given Harmable once ever X milliseconds.
    # That 'X' is called a cooldown.
    damage_cooldown = 1200  # milliseconds
    last_recorded_damage = None

    def is_damage_cooldown_expired(self, target):
        # target is a Harmable

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

class Player(BaseSprite, Harmable):

    hit_points = 100
    speed = 5
    _weapons = None

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/adventurer-idle-02.png").convert()
        self.rect = self.image.get_rect()

    def __str__(self):
        return f"The Player {self.id}"

    def die(self):
        print(f"{self} has died")

    @property
    def weapons(self):
        if self._weapons is None:
            self._weapons = pygame.sprite.Group()
        return self._weapons

class Enemy(BaseSprite, Harmable, Weapon):

    speed = 2
    hit_points = 100
    _damage = 1

    def __init__(self):
        super().__init__()

        if random.randint(1,10) > 2:
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
        destination_x = sprite.position[0] + random.randint(1,sprite.width)
        destination_y = sprite.position[1] + random.randint(1,sprite.height)
        self.move_toward((destination_x, destination_y))

    def die(self):
        print(f"{self} has died")