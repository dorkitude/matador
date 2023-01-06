import pygame
import math

def now():
  return pygame.time.get_ticks()


def distance(p1, p2):
  x1, y1 = p1
  x2, y2 = p2
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)


# Declaring variables to be used through the program

# Set the window size

start_time = now() # exactly when did the program start?
window_size = (1024, 768)

vec = pygame.math.Vector2

PLAYER_BASE_SPEED = 12
SPEED_MODIFIER = 0.04

STARTING_HALO_RADIUS = 75


# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SOFT_YELLOW = (255, 255, 127, 1)

# seconds between each spawn
GLOBAL_SPAWN_RATE = 3

# Set the frame rate
frame_rate = 60
frame_duration = int(1000 / frame_rate)


#  events
EVENT_SPAWNER_COOLDOWN = pygame.USEREVENT + 1


def log(x):
  print(x)