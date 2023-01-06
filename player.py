from globals import *
from sprites import BaseCharacter, Harmable, sprites_to_render_first
from weapons import Halo

class Player(BaseCharacter, Harmable):

    # default values
    hit_points = 100
    speed = PLAYER_BASE_SPEED
    _weapons = None # this will get set the first time the instance property is accessed
    halo = None
    status = None
    stunnable = False

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("sprites/matador.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # make the starting weapon
        self.halo = Halo(self, STARTING_HALO_RADIUS)
        sprites_to_render_first.add(self.halo)
        self.hurt_sound = pygame.mixer.Sound("sounds/ouch.wav")

    def __str__(self):
        return f"Player {self.id}"

    def die(self):
        print(f"{self} has died")
        self.kill()

    def after_damage_taken(self):
        self.hurt_sound.play()

    @property
    def weapons(self):
        if self._weapons is None:
            self._weapons = pygame.sprite.Group()
        return self._weapons

    def update(self, control):
        if self.velocity.length() > 0:
            self.move(self.velocity)

    def after_move(self):
        if self.halo:
            self.halo.x = (self.x + self.width/2) - self.halo.radius
            self.halo.y = (self.y + self.height/2) - self.halo.radius