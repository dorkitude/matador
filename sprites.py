from globals import *

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


class Player(BaseSprite):


    speed = 5

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/adventurer-idle-02.png").convert()
        self.rect = self.image.get_rect()

    @property
    def position(self):
        return (self.x, self.y)

class Enemy(BaseSprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/lizard_f_idle_anim_f3.png").convert()
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "RIGHT"