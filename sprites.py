from globals import *
from abc import ABC, abstractmethod
import random

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

    def distance_to(self, sprite): #float
        return vec(self.rect.center).distance_to(vec(sprite.rect.center))

    def collides_with_any(self, sprite_group): #bool
        return pygame.sprite.spritecollideany(self, sprite_group)

    def move(self, direction, collision_checks=None):   # void
        # this is a method that moves the sprite in the direction of the vector
        # It will check for collisions with other sprites in the collision_checks
        # group.  If a collision is detected, the sprite will attempt to move in
        # the direction of the vector, but will stop before colliding with the other sprite.

        if not collision_checks:
            # make in an empty group
            collision_checks = pygame.sprite.Group()

        if direction.length() == 0:
            return

        # Normalize the direction vector, so we have have a vector of length 1
        direction = direction.normalize()
        magnitude = self.speed * SPEED_MODIFIER * frame_duration

        velocity = vec(direction[0]*magnitude, direction[1]*magnitude)

        old_position = vec(self.x, self.y)
        preferred_destination = old_position + vec(velocity)

        # relocate the sprite
        self.x = preferred_destination[0]
        self.y = preferred_destination[1]

        # use an approximated binary search to get as close as possible to the destination
        # without colliding with the other sprites

        if self.collides_with_any(collision_checks):
            # print(f"{self.id} is doing collision checks")
            # print(f"preffered destination: {preferred_destination}")
            # print(f"old position: {old_position}")
            # print(f"Collision detected at {self.x}, {self.y}")
            # check 90% of the way
            self.x = old_position[0] + 0.9 * (self.x - old_position[0])
            self.y = old_position[1] + 0.9 * (self.y - old_position[1])
            # print(f"checking {self.x}, {self.y}...")

        if self.collides_with_any(collision_checks):
            # print(f"Collision detected at {self.x}, {self.y}")
            # check 80%
            self.x = old_position[0] + 0.8 * (self.x - old_position[0])
            self.y = old_position[1] + 0.8 * (self.y - old_position[1])
            # print(f"checking {self.x}, {self.y}...")

        if self.collides_with_any(collision_checks):
            # print(f"Collision detected at {self.x}, {self.y}")
            # check 20% of the way to the destination
            self.x = old_position[0] + 0.2 * (self.x - old_position[0])
            self.y = old_position[1] + 0.2 * (self.y - old_position[1])
            # print(f"checking {self.x}, {self.y}...")

        if self.collides_with_any(collision_checks):
            # print(f"Collision detected at {self.x}, {self.y}")
            # print(f"Gonna try rotating my motion vector counter-clockwise 90 degrees")
            # try pathfinding by moving orthogonal to the velocity vector
            orthogonal_vector = velocity.rotate(90)
            # print(f"original velocity: {velocity}, orthogonal vector: {orthogonal_vector}")
            orthogonal_destination = old_position + orthogonal_vector
            # print(f"instead of preffered destination: {preferred_destination}, I'm going to try {orthogonal_destination}")
            self.x = orthogonal_destination[0]
            self.y = orthogonal_destination[1]

        if self.collides_with_any(collision_checks):
            # print(f"Collision detected at {self.x}, {self.y}")
            # print(f"Gonna try rotating my motion vector clockwise")
            # try pathfinding by moving in the *opposite* orthogonal direction
            orthogonal_vector = velocity.rotate(-90)
            # print(f"original velocity: {velocity}, orthogonal vector: {orthogonal_vector}")
            orthogonal_destination = old_position + orthogonal_vector
            self.x = orthogonal_destination[0]
            self.y = orthogonal_destination[1]

        if self.collides_with_any(collision_checks):
            # print(f"can't move at all")
            # if we still collide, then we can't move at all
            self.x = old_position[0]
            self.y = old_position[1]
            return None

        # print(f"successfully moved to {self.x}, {self.y}")

        # Keep the sprite within the window boundaries
        if self.x < 0:
            self.x = 0
        if self.x + self.width > window_size[0]:
            self.x = window_size[0] - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > window_size[1]:
            self.y = window_size[1] - self.height

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
        self.after_move()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = value
        self.after_move()

    def after_move(self):
        pass

class Harmable(ABC):
    # This is a mixin that handles hit points and damage

    def take_damage_from(self, weapon):

        if weapon.is_damage_cooldown_expired(self):
            # randomize damage by 12% in either direction
            real_damage = int(weapon.damage * (1 + random.uniform(-0.12, 0.12)))
            self.hit_points -= real_damage
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

class Player(BaseSprite, Harmable):

    # default values
    hit_points = 100
    speed = PLAYER_BASE_SPEED
    _weapons = None # this will get set the first time the instance property is accessed
    halo = None

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/adventurer-idle-02.png").convert()
        self.rect = self.image.get_rect()

    def __str__(self):
        return f"Player {self.id}"

    def die(self):
        print(f"{self} has died")
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



class Enemy(BaseSprite, Harmable, Weapon):

    all_enemies = pygame.sprite.Group()
    resolved_enemies = pygame.sprite.Group()
    pursuing_enemies = pygame.sprite.Group()

    speed = 2
    hit_points = 10
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

        Enemy.all_enemies.add(self)

    @property
    def damage(self):
        return self._damage

    def __str__(self):
        return f"An Enemy {self.id}"

    def pursue(self, sprite):
        destination_x = sprite.position[0] + random.randint(1,sprite.width)
        destination_y = sprite.position[1] + random.randint(1,sprite.height)
        direction = vec((destination_x-self.x, destination_y-self.y))
        self.move(direction, Enemy.resolved_enemies)

    def die(self):
        print(f"{self} has died")
        print(len(Enemy.all_enemies.sprites()))
        self.kill()  # TODO:  figure out how to
        print(len(Enemy.all_enemies.sprites()))