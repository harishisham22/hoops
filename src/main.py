import pygame
import sys
from entities.player import Player
from entities.ball import Ball
from entities.hoop import Hoop
from constants import *

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2D Basketball Game")
    clock = pygame.time.Clock()

    # Create game objects
    player = Player(WINDOW_HEIGHT)
    ball = Ball(WINDOW_HEIGHT)
    hoop = Hoop(WINDOW_WIDTH, WINDOW_HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and player.has_ball:  # Left click to shoot
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    ball.shoot(player.x + player.width/2, player.y - 20, mouse_x, mouse_y)
                    player.has_ball = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.has_ball:  # Space to drop ball
                    player.has_ball = False
                    ball.active = True
                    ball.velocity_y = -5  # Small upward velocity when dropping

        # Get keyboard input
        keys = pygame.key.get_pressed()
        player.move(keys, ball, WINDOW_WIDTH)

        # Update game objects
        player.update(WINDOW_WIDTH, WINDOW_HEIGHT)
        ball.update(player, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Check for scoring
        if hoop.check_score(ball):
            ball.reset()
            player.has_ball = False

        # Draw everything
        screen.fill(COURT_COLOR)
        player.draw(screen)
        ball.draw(screen)
        hoop.draw(screen)

        # Draw cursor position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.circle(screen, WHITE, (mouse_x, mouse_y), 5)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main() 