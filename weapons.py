from globals import *
from sprites import BaseSprite, Weapon, sprites_to_render_first
import pygame

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