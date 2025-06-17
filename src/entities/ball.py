import pygame
import math

class Ball:
    def __init__(self, window_height):
        self.window_height = window_height
        self.reset()

    def reset(self):
        self.radius = 15
        self.x = 150
        self.y = self.window_height - self.radius
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

    def update(self, player, window_width, window_height):
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
        if self.y > window_height - self.radius * 2:
            self.y = window_height - self.radius * 2
            self.velocity_y = -self.velocity_y * self.bounce_damping
            self.velocity_x *= self.bounce_damping

        # Screen boundaries with bouncing
        if self.x < self.radius:
            self.x = self.radius
            self.velocity_x = -self.velocity_x * self.bounce_damping
        elif self.x > window_width - self.radius:
            self.x = window_width - self.radius
            self.velocity_x = -self.velocity_x * self.bounce_damping

        # Ceiling collision
        if self.y < self.radius:
            self.y = self.radius
            self.velocity_y = -self.velocity_y * self.bounce_damping

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.radius) 