import pygame

# Declaring variables to be used through the program
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

SPEED_MODIFIER = 0.05

# Set the frame rate
frame_rate = 60
frame_duration = int(1000 / frame_rate)

# Set the window size
window_size = (800, 600)


EVENT_SPAWNER_COOLDOWN = pygame.USEREVENT + 1