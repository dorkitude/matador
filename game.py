from math import ceil
from globals import *
import ui
from control import Control
from sprites import Enemy, sprites_to_render_first, sprites_to_render_second, sprites_to_render_third, sprites_to_render_fourth

# Initialize Pygame
control = Control()

# Create the window
screen = pygame.display.set_mode(window_size)

# this schedules a reccurring event to spawn enemies
pygame.time.set_timer(EVENT_SPAWNER_COOLDOWN, ceil(1000*GLOBAL_SPAWN_RATE))

running = True
while running:

    control.update()

    # -------------------
    # Update the display
    # -------------------

    # show/update player HP bar in top-peft
    ui.render_player_stats(control.player)

    # first, handle map and background stuff
    control.setup_background()

    # next, render floor-level stuff
    for sprite in sprites_to_render_first:
        sprite.render(screen)

    for sprite in sprites_to_render_second:
        sprite.render(screen)

    for sprite in sprites_to_render_third:
        sprite.render(screen)

    for sprite in sprites_to_render_fourth:
        sprite.render(screen)

    pygame.display.update()

    Enemy.resolved_enemies.empty()

    # Wait for the next frame
    pygame.time.delay(frame_duration)