import pygame
from globals import *
from abc import ABC, abstractmethod
from base_sprites import BaseSprite


class TextSprite(BaseSprite):

    def __init__(self, text, position, font_size=24, color=WHITE, dissolve_timer=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, self.font_size)
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.dissolve_timer = dissolve_timer
        self.x = position[0]
        self.y = position[1]

        if dissolve_timer:
            self.dissolve_at = now() + dissolve_timer

    def render(self, screen):
        if self.dissolve_timer:
            timer_remaining = self.dissolve_at - now()

            if timer_remaining > 0:
                # fade out the text
                alpha = int(255 * (timer_remaining / self.dissolve_timer))
                # self.image.set_alpha(alpha)
            else:
                # kill the sprite
                self.kill()

        super().render(screen)

    def drift(self):
        # animate the text drifting up
        pass