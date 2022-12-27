import pygame

def now():
  return pygame.time.get_ticks()

start_time = now()

# Declaring variables to be used through the program
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

PLAYER_BASE_SPEED = 7
SPEED_MODIFIER = 0.05

STARTING_HALO_RADIUS = 50

# seconds between each spawn
GLOBAL_SPAWN_RATE = 3

# Set the frame rate
frame_rate = 60
frame_duration = int(1000 / frame_rate)

# Set the window size
window_size = (800, 600)

#  events
EVENT_SPAWNER_COOLDOWN = pygame.USEREVENT + 1


def log(x):
  print(x)