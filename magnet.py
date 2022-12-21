import pygame
from models import Foo

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (600, 400)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title
pygame.display.set_caption("Metal Ball")

# Set the frame rate
frame_rate = 60
frame_duration = int(1000 / frame_rate)

# initial state

# Make the ball
ball = Foo()
ball.radius = 20
ball.x = 300
ball.y = 200
ball.vel_x = 5  # Initial velocity (move right)
ball.vel_y = 5  # Initial velocity (move down)

# Set the hole properties
hole = Foo()
hole.radius = 20
hole.x = 500
hole.y = 300

# make the magnet
magnet = Foo()
magnet.width = 50
magnet.height = 25
magnet.x = 300
magnet.y = 350
magnet.vel_x = 0  # Initial velocity (no movement)
magnet.vel_y = 0  # Initial velocity (no movement)


# make the stage
stage = Foo()

# colors
ball.color = (200, 200, 200)
hole.color = (0, 0, 0,)
stage.color = (0, 100, 0)
magnet.color = (0, 255, 0)  # Green



# Run the game loop
running = True
while running:
  # Handle events
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False


  # Handle key input
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
      magnet.vel_x = -5  # Move left
  elif keys[pygame.K_RIGHT]:
      magnet.vel_x = 5  # Move right
  else:
      magnet.vel_x = 0  # Stop movement
  if keys[pygame.K_UP]:
      magnet.vel_y = -5  # Move up
  elif keys[pygame.K_DOWN]:
      magnet.vel_y = 5  # Move down
  else:
      magnet.vel_y = 0  # Stop movement

  # Update the magnet position
  magnet.x += magnet.vel_x
  magnet.y += magnet.vel_y

  # Keep the magnet within the window boundaries
  if magnet.x < 0:
      magnet.x = 0
  if magnet.x + magnet.width > window_size[0]:
      magnet.x = window_size[0] - magnet.width
  if magnet.y < 0:
      magnet.y = 0
  if magnet.y + magnet.height > window_size[1]:
      magnet.y = window_size[1] - magnet.height


  # Update the game state
  # ...

  # Update the ball position
  ball.x += ball.vel_x
  ball.y += ball.vel_y

  # Check for ball collision with the walls
  if ball.x - ball.radius < 0 or ball.x + ball.radius > window_size[0]:
      ball.vel_x *= -1  # Reverse the horizontal velocity
  if ball.y - ball.radius < 0 or ball.y + ball.radius > window_size[1]:
      ball.vel_y *= -1  # Reverse the vertical velocity

  # Draw the game
  # ...
  # Clear the screen
  screen.fill(stage.color)

  # Draw the magnet
  # Calculate the points of the U-shaped magnet
  magnet.points = [
      (magnet.x, magnet.y),
      (magnet.x + magnet.width / 2, magnet.y - magnet.height),
      (magnet.x + magnet.width, magnet.y),
      (magnet.x + magnet.width / 2, magnet.y + magnet.height),
  ]

  # Draw the magnet
  pygame.draw.polygon(screen, magnet.color, magnet.points)


  # Draw the ball
  pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.radius)

  # Draw the hole
  pygame.draw.circle(screen, hole.color, (hole.x, hole.y), hole.radius)

  pygame.display.update()


  # Wait for the next frame
  pygame.time.delay(frame_duration)
