import pygame

def now():
  return pygame.time.get_ticks()


# Declaring variables to be used through the program

# Set the window size

start_time = now() # exactly when did the program start?
window_size = (1024, 768)

vec = pygame.math.Vector2
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

PLAYER_BASE_SPEED = 8
SPEED_MODIFIER = 0.04

STARTING_HALO_RADIUS = 50


# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# seconds between each spawn
GLOBAL_SPAWN_RATE = 3

# Set the frame rate
frame_rate = 60
frame_duration = int(1000 / frame_rate)


#  events
EVENT_SPAWNER_COOLDOWN = pygame.USEREVENT + 1


def log(x):
  print(x)