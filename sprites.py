from globals import *
import math

class Foo(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
class BaseSprite(pygame.sprite.Sprite):
    _width = None
    _height = None

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

    def move(self, direction):
        # Normalize the direction vector, so we have have a vector of length 1
        direction = direction.normalize()
        magnitude = self.speed * SPEED_MODIFIER * frame_duration

        velocity = vec(direction[0]*magnitude, direction[1]*magnitude)

        new_position = self.position + velocity
        self.x = new_position[0]
        self.y = new_position[1]

        # Keep the player within the window boundaries
        if self.x < 0:
            self.x = 0
        if self.x + self.width > window_size[0]:
            self.x = window_size[0] - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > window_size[1]:
            self.y = window_size[1] - self.height

    def move_toward(self, destination):
        # Update the player position
        direction = vec((destination[0]-self.x, destination[1]-self.y))
        self.move(direction)

    @property
    def position(self):
        return (self.x, self.y)



class Player(BaseSprite):

    speed = 5

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/adventurer-idle-02.png").convert()
        self.rect = self.image.get_rect()

class Enemy(BaseSprite):

    speed = 2

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/lizard_f_idle_anim_f3.png").convert()
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = vec(340, 240)
