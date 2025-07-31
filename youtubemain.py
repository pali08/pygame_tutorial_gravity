import pygame
import sys

pygame.init()

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((800, 800))
CURRENT_DIRECTION = "right"
pygame.display.set_caption("Jumping in PyGame")

X_POSITION, Y_POSITION = 400, 660

jumping = False

Y_GRAVITY = 0.6
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT

STANDING_SURFACE_RIGHT = pygame.transform.scale(pygame.image.load("assets/mario_standing_right.png"), (48, 64))
STANDING_SURFACE_LEFT = pygame.transform.scale(pygame.image.load("assets/mario_standing_left.png"), (48, 64))

JUMPING_SURFACE_RIGHT = pygame.transform.scale(pygame.image.load("assets/mario_jumping_right.png"), (48, 64))
JUMPING_SURFACE_LEFT = pygame.transform.scale(pygame.image.load("assets/mario_jumping_left.png"), (48, 64))

BACKGROUND = pygame.image.load("assets/background.png")

mario_rect = STANDING_SURFACE_RIGHT.get_rect(center=(X_POSITION, Y_POSITION))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_SPACE]:
        jumping = True


    SCREEN.blit(BACKGROUND, (0, 0))
    
    if jumping:
        Y_VELOCITY -= Y_GRAVITY
        Y_POSITION -= Y_VELOCITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT
            Y_POSITION = 660
        if CURRENT_DIRECTION == "right":
            jumping_surface = JUMPING_SURFACE_RIGHT
        elif CURRENT_DIRECTION == "left":
            jumping_surface = JUMPING_SURFACE_LEFT
        if keys_pressed[pygame.K_LEFT]:
            X_POSITION -= 5
            CURRENT_DIRECTION = "left"
        if keys_pressed[pygame.K_RIGHT]:
            X_POSITION += 5
            CURRENT_DIRECTION = "right"
        mario_rect = jumping_surface.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(jumping_surface, mario_rect)
    else:
        if CURRENT_DIRECTION == "right":
            standing_surface = STANDING_SURFACE_RIGHT
        elif CURRENT_DIRECTION == "left":
            standing_surface = STANDING_SURFACE_LEFT
        mario_rect = standing_surface.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(standing_surface, mario_rect)

        if keys_pressed[pygame.K_LEFT]:
            X_POSITION -= 5
            mario_rect = STANDING_SURFACE_LEFT.get_rect(center=(X_POSITION, Y_POSITION))
            SCREEN.blit(STANDING_SURFACE_LEFT, mario_rect)
            CURRENT_DIRECTION = "left"

        if keys_pressed[pygame.K_RIGHT]:
            X_POSITION += 5
            mario_rect = STANDING_SURFACE_RIGHT.get_rect(center=(X_POSITION, Y_POSITION))
            SCREEN.blit(STANDING_SURFACE_RIGHT, mario_rect)
            CURRENT_DIRECTION = "right"


    pygame.display.update()
    CLOCK.tick(60)