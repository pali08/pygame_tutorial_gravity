import pygame
import sys

pygame.init()

# Constants
CLOCK = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumping in PyGame")
Y_GROUND_POSITION = 660
X_POSITION, Y_POSITION = 400, Y_GROUND_POSITION  # start on ground, top-left
JUMP_SPEED = -20
Y_GRAVITY = 0.6
X_SPEED = 5
MARIO_WIDTH, MARIO_HEIGHT = 48, 64

# Game Variables
current_direction = "right"
jumping = False
y_velocity = 0

# Asset Loading
def load_image(path, size):
    return pygame.transform.scale(pygame.image.load(path), size)

STANDING_SURFACE_RIGHT = load_image("assets/mario_standing_right.png", (MARIO_WIDTH, MARIO_HEIGHT))
STANDING_SURFACE_LEFT = load_image("assets/mario_standing_left.png", (MARIO_WIDTH, MARIO_HEIGHT))
JUMPING_SURFACE_RIGHT = load_image("assets/mario_jumping_right.png", (MARIO_WIDTH, MARIO_HEIGHT))
JUMPING_SURFACE_LEFT = load_image("assets/mario_jumping_left.png", (MARIO_WIDTH, MARIO_HEIGHT))
PLATFORM = load_image("assets/platform.jpg", (MARIO_WIDTH * 4, MARIO_HEIGHT))
BACKGROUND = pygame.image.load("assets/background.png")

# Rectangles
mario_rect = STANDING_SURFACE_RIGHT.get_rect(center=(X_POSITION, Y_POSITION))
platform_rect =  PLATFORM.get_rect(center=(SCREEN_WIDTH/2, 460))

# Helper Functions
def update_position(direction, x, y, jumping):
    """Update Mario's position and return new rectangle and surface."""
    if direction == "right":
        surface = JUMPING_SURFACE_RIGHT if jumping else STANDING_SURFACE_RIGHT
    else:
        surface = JUMPING_SURFACE_LEFT if jumping else STANDING_SURFACE_LEFT
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

def handle_jumping(keys, _jumping, _y_velocity, _y_position, _player_rect, _platform_rect):
    """Handle Mario's jumping logic and return updated values."""
    # Start jump
    print(_y_velocity)
    # Can only jump if standing on ground/platform
    on_ground = (_player_rect.bottom >= Y_GROUND_POSITION) or (
            _player_rect.colliderect(_platform_rect)
            and _platform_rect.left <= _player_rect.centerx <= _platform_rect.right
            and _player_rect.bottom <= _platform_rect.top + 5  # small tolerance
    )

    if keys[pygame.K_SPACE] and on_ground:
        _y_velocity = JUMP_SPEED
        _jumping = True

    # Gravity
    _y_velocity += Y_GRAVITY
    _y_position += _y_velocity
    _player_rect.topleft = (_player_rect.x, _y_position)

    # Platform collision (only when falling)
    print(_y_velocity)

    if _player_rect.colliderect(platform_rect) and _y_velocity >= 0:
        if platform_rect.left <= _player_rect.centerx <= platform_rect.right:
            _y_position = platform_rect.top - MARIO_HEIGHT / 2
            _y_velocity = 0
            _jumping = False

    # Ground collision (only when falling)
    elif _player_rect.bottom >= Y_GROUND_POSITION and _y_velocity >= 0:
        _y_position = Y_GROUND_POSITION
        _y_velocity = 0
        _jumping = False

    return _jumping, _y_velocity, _y_position

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()

    jumping, y_velocity, Y_POSITION = handle_jumping(
        keys_pressed, jumping, y_velocity, Y_POSITION, mario_rect, platform_rect
    )
    X_POSITION, current_direction = handle_movement(keys_pressed, X_POSITION, current_direction)

    # Draw Everything
    SCREEN.blit(BACKGROUND, (0, 0))
    mario_rect, mario_surface = update_position(current_direction, X_POSITION, Y_POSITION, jumping)
    SCREEN.blit(mario_surface, mario_rect)
    SCREEN.blit(PLATFORM, platform_rect)

    pygame.display.update()
    CLOCK.tick(60)