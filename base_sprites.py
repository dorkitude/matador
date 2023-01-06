import pygame
from globals import *
from abc import ABC, abstractmethod

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

    def distance_to(self, sprite): #float
        return vec(self.rect.center).distance_to(vec(sprite.rect.center))

    def move(self, direction, collision_checks=None, speed_scalar=1):   # void
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
        magnitude = self.speed * speed_scalar * SPEED_MODIFIER * frame_duration

        velocity = vec(direction[0]*magnitude, direction[1]*magnitude)

        old_position = vec(self.x, self.y)
        preferred_destination = old_position + vec(velocity)

        # relocate the sprite
        self.x = preferred_destination[0]
        self.y = preferred_destination[1]

        if self.collides_with_any(collision_checks):
            self.x = old_position[0] + 0.9 * (self.x - old_position[0])
            self.y = old_position[1] + 0.9 * (self.y - old_position[1])

        if self.collides_with_any(collision_checks):
            self.x = old_position[0] + 0.8 * (self.x - old_position[0])
            self.y = old_position[1] + 0.8 * (self.y - old_position[1])

        rotation_angles = [15, 30, 45, 60, 75, 90, -15, -30, -45, -60, -75, -90, 180]

        for angle in rotation_angles:
            if self.collides_with_any(collision_checks):
                rotated_vector = velocity.rotate(angle)
                attempted_destination = old_position + rotated_vector
                self.x = attempted_destination[0]
                self.y = attempted_destination[1]
                # if not self.collides_with_any(collision_checks):
                    # print(f"rotating by {angle}º worked!")
            else:
                break

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

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def after_move(self):
        pass

    def collides_with(self, sprite): #bool
        return self.rect.colliderect(sprite.rect)

    def collides_with_any(self, sprite_group): #bool
        return pygame.sprite.spritecollideany(self, sprite_group)

class BaseCharacter(BaseSprite, ABC):
    pass

class BaseParticle(BaseSprite, ABC):
    pass