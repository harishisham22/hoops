import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200  # Increased width for full court
WINDOW_HEIGHT = 800  # Increased height for full court
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
COURT_COLOR = (50, 50, 50)  # Dark gray for court

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2D Basketball Game")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x = 160
        self.y = WINDOW_HEIGHT - 60
        self.width = 40
        self.height = 60
        self.speed = 5
        self.jumping = False
        self.jump_power = 15
        self.velocity_y = 0
        self.gravity = 0.8
        self.has_ball = False
        self.dribbling = False
        self.dribble_height = 0
        self.dribble_direction = 1
        # Double tap tracking
        self.last_a_press = 0
        self.last_w_press = 0
        self.double_tap_window = 300  # milliseconds
        self.dash_cooldown = 500  # milliseconds
        self.last_dash_time = 0
        self.dash_speed = 15
        self.dash_duration = 200  # milliseconds
        self.dash_start_time = 0
        self.is_dashing = False

    def move(self, keys, ball):
        current_time = pygame.time.get_ticks()
        
        # Handle double tap dash
        if keys[pygame.K_a] and not self.is_dashing:
            if current_time - self.last_a_press < self.double_tap_window and current_time - self.last_dash_time > self.dash_cooldown:
                self.is_dashing = True
                self.dash_start_time = current_time
                self.last_dash_time = current_time
            self.last_a_press = current_time
            self.x -= self.speed
            if self.has_ball:
                self.dribble_direction = -1
                
        if keys[pygame.K_d] and not self.is_dashing:
            self.x += self.speed
            if self.has_ball:
                self.dribble_direction = 1

        # Handle dash movement
        if self.is_dashing:
            if current_time - self.dash_start_time < self.dash_duration:
                self.x -= self.dash_speed  # Dash left
            else:
                self.is_dashing = False

        # Jump with potential double tap dash
        if keys[pygame.K_w] and not self.jumping:
            if current_time - self.last_w_press < self.double_tap_window and current_time - self.last_dash_time > self.dash_cooldown:
                # Vertical dash
                self.velocity_y = -self.jump_power * 1.5
                self.last_dash_time = current_time
            else:
                self.velocity_y = -self.jump_power
            self.jumping = True
            self.last_w_press = current_time

        # Handle ball possession
        if self.has_ball:
            ball.x = self.x + self.width/2
            ball.y = self.y - 20 + self.dribble_height
            if not self.jumping:
                self.dribble_height = 10 * math.sin(pygame.time.get_ticks() * 0.01)
            else:
                self.dribble_height = 0
                ball.y = self.y - 20

    def update(self):
        # Apply gravity
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Ground collision
        if self.y > WINDOW_HEIGHT - 60:  # Adjusted ground level
            self.y = WINDOW_HEIGHT - 60
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
        self.radius = 15
        self.x = 150
        self.y = WINDOW_HEIGHT - self.radius  # Adjusted to be at player's level
        self.velocity_x = 0
        self.velocity_y = 0
        self.active = False
        self.power = 0
        self.angle = 0
        self.bounce_damping = 0.5

    def shoot(self, start_x, start_y, target_x, target_y):
        self.active = True
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx * dx + dy * dy)
        power = min(distance * 0.1, 20)  # Scale power based on distance, max 20
        angle = math.atan2(-dy, dx)  # Negative dy because y is inverted in pygame
        self.velocity_x = power * math.cos(angle)
        self.velocity_y = -power * math.sin(angle)

    def update(self, player):
        if not self.active:
            # Check if ball is close enough to player to be caught
            dx = self.x - (player.x + player.width/2)
            dy = self.y - (player.y - 20)
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < 30 and not player.has_ball:
                player.has_ball = True
                self.active = False
            return

        self.velocity_y += 0.5  # Gravity
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Ground collision
        if self.y > WINDOW_HEIGHT - self.radius * 2:
            self.y = WINDOW_HEIGHT - self.radius * 2
            self.velocity_y = -self.velocity_y * self.bounce_damping
            self.velocity_x *= self.bounce_damping

        # Screen boundaries with bouncing
        if self.x < self.radius:
            self.x = self.radius
            self.velocity_x = -self.velocity_x * self.bounce_damping
        elif self.x > WINDOW_WIDTH - self.radius:
            self.x = WINDOW_WIDTH - self.radius
            self.velocity_x = -self.velocity_x * self.bounce_damping

        # Ceiling collision
        if self.y < self.radius:
            self.y = self.radius
            self.velocity_y = -self.velocity_y * self.bounce_damping

    def draw(self, screen):
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius)

class Hoop:
    def __init__(self):
        self.x = WINDOW_WIDTH - 300  # Adjusted position for new court size
        self.y = WINDOW_HEIGHT - 250  # Adjusted position for new court size
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
        player.move(keys, ball)

        # Update game objects
        player.update()
        ball.update(player)

        # Check for scoring
        if hoop.check_score(ball):
            ball.reset()
            player.has_ball = False

        # Draw everything
        screen.fill(COURT_COLOR)  # Fill with court color
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