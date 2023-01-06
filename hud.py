from globals import *
from pygame.font import Font
from text_sprite import TextSprite


class Hud(object):
    def __init__(self, **kwargs):
      self.__dict__.update(kwargs)
      self.surface = pygame.Surface((window_size[0], 100))

    def update(self):
      pass

    def render(self, screen, control):
        self.surface.fill(BLACK)

        # print(f"rendering player stats")

        # render the player's health
        health_bar = pygame.Surface((max(0, control.player.hit_points), 20))

        hit_points = TextSprite(
            text=f"{control.player.hit_points}",
            position=(10, 10),
            font_size=24,
            color=WHITE,

        )

        health_bar.fill(RED)
        health_bar.blit(hit_points.image, (0, 0))

        # render the player's health
        self.surface.blit(health_bar, (10, 10))


        screen.blit(self.surface, (0, 0))