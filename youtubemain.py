import pygame
import sys

pygame.init()

# Constants
CLOCK = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumping in PyGame")
Y_GROUND_POSITION = 660
X_POSITION, Y_POSITION = 400, Y_GROUND_POSITION
JUMP_HEIGHT = 20
Y_GRAVITY = 0.6
X_SPEED = 5
MARIO_WIDTH, MARIO_HEIGHT = 48, 64

# Game Variables
current_direction = "right"
jumping = False
y_velocity = JUMP_HEIGHT


# Asset Loading
def load_image(path, size):
    return pygame.transform.scale(pygame.image.load(path), size)


# Constants for dimensions
MARIO_WIDTH, MARIO_HEIGHT = 48, 64

# Usage of constants in asset loading
STANDING_SURFACE_RIGHT = load_image("assets/mario_standing_right.png", (MARIO_WIDTH, MARIO_HEIGHT))
STANDING_SURFACE_LEFT = load_image("assets/mario_standing_left.png", (MARIO_WIDTH, MARIO_HEIGHT))
JUMPING_SURFACE_RIGHT = load_image("assets/mario_jumping_right.png", (MARIO_WIDTH, MARIO_HEIGHT))
JUMPING_SURFACE_LEFT = load_image("assets/mario_jumping_left.png", (MARIO_WIDTH, MARIO_HEIGHT))
BACKGROUND = pygame.image.load("assets/background.png")

# Current Position Rectangle
mario_rect = STANDING_SURFACE_RIGHT.get_rect(center=(X_POSITION, Y_POSITION))


# Helper Functions
def update_position(direction, x, y):
    """Update Mario's position and return new rectangle and surface."""
    if direction == "right":
        if not jumping:
            surface = STANDING_SURFACE_RIGHT
        else:
            surface = JUMPING_SURFACE_RIGHT
    else:
        if not jumping:
            surface = STANDING_SURFACE_LEFT
        else:
            surface = JUMPING_SURFACE_LEFT
    rect = surface.get_rect(center=(x, y))
    return rect, surface


def handle_movement(keys, x, direction):
    """Update X_POSITION and CURRENT_DIRECTION based on arrow key inputs."""
    if keys[pygame.K_LEFT] and x > (MARIO_WIDTH/2):
        x -= X_SPEED
        direction = "left"
    if keys[pygame.K_RIGHT] and x < SCREEN_WIDTH - (MARIO_WIDTH/2):
        x += X_SPEED
        direction = "right"
    return x, direction


def handle_jumping(keys, jumping, y_velocity, y_position):
    """Handle Mario's jumping logic and return updated values."""
    if keys[pygame.K_SPACE] and not jumping:
        jumping = True

    if jumping:
        y_velocity -= Y_GRAVITY
        y_position -= y_velocity
        if y_velocity < -JUMP_HEIGHT:
            jumping = False
            y_velocity = JUMP_HEIGHT
            y_position = Y_GROUND_POSITION  # Reset to ground

    return jumping, y_velocity, y_position


# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()

    jumping, y_velocity, Y_POSITION = handle_jumping(keys_pressed, jumping, y_velocity, Y_POSITION)
    X_POSITION, current_direction = handle_movement(keys_pressed, X_POSITION, current_direction)

    # Draw Everything
    SCREEN.blit(BACKGROUND, (0, 0))
    mario_rect, mario_surface = update_position(current_direction, X_POSITION, Y_POSITION)
    SCREEN.blit(mario_surface, mario_rect)

    pygame.display.update()
    CLOCK.tick(60)
