import pygame
from globals import *
from abc import ABC, abstractmethod
from base_sprites import BaseSprite


class TextSprite(BaseSprite):

    def __init__(self, text, position, font_size=24, color=WHITE, dissolve_after=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, self.font_size)
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.x = position[0]
        self.y = position[1]

        if dissolve_after:
            self.dissolve_after = now() + dissolve_after

    def render(self, screen):
        super().render(screen)

        if now() > self.dissolve_after:
            self.kill()


    def drift(self):
        # animate the text drifting up
        pass