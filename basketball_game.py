import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2D Basketball Game")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x = 100
        self.y = WINDOW_HEIGHT - 100
        self.width = 40
        self.height = 60
        self.speed = 5
        self.jumping = False
        self.jump_power = 15
        self.velocity_y = 0
        self.gravity = 0.8

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.velocity_y = -self.jump_power

    def update(self):
        # Apply gravity
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Ground collision
        if self.y > WINDOW_HEIGHT - 100:
            self.y = WINDOW_HEIGHT - 100
            self.jumping = False
            self.velocity_y = 0

        # Screen boundaries
        if self.x < 0:
            self.x = 0
        if self.x > WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 150
        self.y = WINDOW_HEIGHT - 80
        self.radius = 15
        self.velocity_x = 0
        self.velocity_y = 0
        self.active = False
        self.power = 0
        self.angle = 0

    def shoot(self, power, angle):
        self.active = True
        self.velocity_x = power * math.cos(math.radians(angle))
        self.velocity_y = -power * math.sin(math.radians(angle))

    def update(self):
        if self.active:
            self.velocity_y += 0.5  # Gravity
            self.x += self.velocity_x
            self.y += self.velocity_y

            # Ground collision
            if self.y > WINDOW_HEIGHT - self.radius:
                self.reset()

            # Screen boundaries
            if self.x < self.radius or self.x > WINDOW_WIDTH - self.radius:
                self.velocity_x *= -0.8

    def draw(self, screen):
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius)

class Hoop:
    def __init__(self):
        self.x = WINDOW_WIDTH - 200
        self.y = WINDOW_HEIGHT - 200
        self.width = 80
        self.height = 60
        self.rim_width = 60
        self.rim_height = 5

    def draw(self, screen):
        # Draw backboard
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        # Draw rim
        pygame.draw.rect(screen, RED, (self.x + 10, self.y + 40, self.rim_width, self.rim_height))

    def check_score(self, ball):
        if (ball.x > self.x + 10 and ball.x < self.x + 70 and
            ball.y > self.y + 40 and ball.y < self.y + 45 and
            ball.velocity_y > 0):
            return True
        return False

def main():
    player = Player()
    ball = Ball()
    hoop = Hoop()
    shooting = False
    power = 0
    angle = 45

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not ball.active:
                    shooting = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and shooting:
                    shooting = False
                    ball.shoot(power, angle)
                    power = 0

        # Handle shooting mechanics
        if shooting and not ball.active:
            power = min(power + 0.5, 20)

        # Get keyboard input
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Update game objects
        player.update()
        ball.update()

        # Check for scoring
        if hoop.check_score(ball):
            ball.reset()

        # Draw everything
        screen.fill(WHITE)
        player.draw(screen)
        ball.draw(screen)
        hoop.draw(screen)

        # Draw power meter when shooting
        if shooting and not ball.active:
            pygame.draw.rect(screen, RED, (10, 10, power * 10, 20))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main() 